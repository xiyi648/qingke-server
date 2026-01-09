#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <cmath>
#include <iomanip>
#include <algorithm>
#include <omp.h>
#include <cstdlib>
#include <cstdint>
#include <thread>
#include <stdexcept>
#include <tuple>
#include <cassert>

// 3D伊辛模型蒙特卡洛模拟（OpenMP并行加速）
#ifndef _OPENMP
#error "This code requires OpenMP support. Compile with -fopenmp (GCC) or /openmp (MSVC)."
#endif

// 模拟常量定义
const int L = 64;
const int n_steps_base = 2000;
const int n_steps_critical = 10000;
const int n_sample = 100;
const int sample_interval = 50;
const double den_start = 5.0;
const double den_end = 4.0;
const double den_step = -0.1;
const double beta_c = 0.2216;
const double den_c = 1.0 / beta_c;
const double critical_window = 0.1;
const size_t max_memory_mb = 2048;
const int default_threads = 4;

// 并行初始化自旋网格（±1随机分布）
void init_spin(std::vector<int>& spin, std::mt19937& rng, int idx) {
    int n_total = L * L * L;
    int max_threads = omp_get_max_threads();
    std::vector<unsigned int> seeds(max_threads);
    std::seed_seq seq{static_cast<unsigned int>(rng()), 
                      static_cast<unsigned int>(std::chrono::high_resolution_clock::now().time_since_epoch().count()), 
                      static_cast<unsigned int>(max_threads), 
                      static_cast<unsigned int>(idx)};
    seq.generate(seeds.data(), seeds.data() + seeds.size());

    #pragma omp parallel
    {
        int tid = omp_get_thread_num();
        std::mt19937 rng_thread(seeds[tid]);
        std::uniform_int_distribution<int> spin_dist(0, 1);
        #pragma omp for schedule(static)
        for (int n = 0; n < n_total; ++n) {
            spin[n] = spin_dist(rng_thread) ? 1 : -1;
        }
    }
}

// Metropolis算法核心：计算给定beta下的平均磁化强度
double ising_3d_metropolis(double beta, std::mt19937& rng, std::vector<int>& spin, int idx) {
    int n_total = L * L * L;
    double den = 1.0 / beta;
    double rel_diff = std::abs((den - den_c) / den_c);
    int n_steps_eff = (rel_diff < critical_window) ? n_steps_critical : n_steps_base;
    int required_steps = n_sample * sample_interval;

    while (n_steps_eff < required_steps) {
        n_steps_eff *= 2;
    }

    int max_threads = omp_get_max_threads();
    std::vector<unsigned int> seeds(max_threads);
    std::seed_seq seq{static_cast<unsigned int>(rng()), 
                      static_cast<unsigned int>(std::chrono::high_resolution_clock::now().time_since_epoch().count()), 
                      static_cast<unsigned int>(max_threads), 
                      static_cast<unsigned int>(idx), 
                      static_cast<unsigned int>(beta * 1000000)};
    seq.generate(seeds.data(), seeds.data() + seeds.size());

    std::vector<int> delta_Es(n_total);
    std::vector<double> mag_samples(n_sample, 0.0);

    #pragma omp parallel
    {
        int tid = omp_get_thread_num();
        std::mt19937 rng_thread(seeds[tid]);
        std::uniform_real_distribution<double> prob_dist_thread(0.0, 1.0);

        for (int step = 0; step < n_steps_eff; ++step) {
            #pragma omp for schedule(static)
            for (int n = 0; n < n_total; ++n) {
                int i = n / (L * L);
                int j = (n / L) % L;
                int k = n % L;

                int i_prev = (i - 1 + L) % L;
                int i_next = (i + 1) % L;
                int j_prev = (j - 1 + L) % L;
                int j_next = (j + 1) % L;
                int k_prev = (k - 1 + L) % L;
                int k_next = (k + 1) % L;

                int idx_prev_i = i_prev * L * L + j * L + k;
                int idx_next_i = i_next * L * L + j * L + k;
                int idx_prev_j = i * L * L + j_prev * L + k;
                int idx_next_j = i * L * L + j_next * L + k;
                int idx_prev_k = i * L * L + j * L + k_prev;
                int idx_next_k = i * L * L + j * L + k_next;

                int nb_sum = spin[idx_prev_i] + spin[idx_next_i] + spin[idx_prev_j] + spin[idx_next_j] + spin[idx_prev_k] + spin[idx_next_k];
                delta_Es[n] = 2 * spin[n] * nb_sum;
            }

            #pragma omp for schedule(static)
            for (int n = 0; n < n_total; ++n) {
                int delta_E = delta_Es[n];
                double arg = beta * static_cast<double>(delta_E);
                if (delta_E <= 0 || prob_dist_thread(rng_thread) < exp(-std::min(arg, 709.0))) {
                    spin[n] *= -1;
                }
            }

            #pragma omp single
            {
                if (step >= n_steps_eff - required_steps && (step - (n_steps_eff - required_steps)) % sample_interval == 0) {
                    int idx_sample = (step - (n_steps_eff - required_steps)) / sample_interval;
                    if (idx_sample < n_sample) {
                        double mag_total = 0.0;
                        #pragma omp for reduction(+:mag_total) schedule(static)
                        for (int n = 0; n < n_total; ++n) {
                            mag_total += spin[n];
                        }
                        mag_samples[idx_sample] = std::fabs(mag_total) / static_cast<double>(n_total);
                    }
                }
            }
        }
    }

    double mag_avg = 0.0;
    for (double mag : mag_samples) {
        mag_avg += mag;
    }
    mag_avg /= static_cast<double>(n_sample);
    return mag_avg;
}

int main() {
    try {
        if (L <= 0) { std::cerr << "Error: L must be a positive integer." << std::endl; return EXIT_FAILURE; }
        if (den_step == 0.0) { std::cerr << "Error: den_step cannot be zero." << std::endl; return EXIT_FAILURE; }
        if (n_sample <= 0 || sample_interval <= 0) { std::cerr << "Error: n_sample and sample_interval must be positive." << std::endl; return EXIT_FAILURE; }

        // 设置并行线程数（优先物理核心）
        int max_threads_hw = omp_get_num_procs();
        int phys_cores = max_threads_hw / 2;
        int use_threads = std::min(default_threads, phys_cores > 0 ? phys_cores : max_threads_hw);
        if (use_threads <= 0) use_threads = 1;
        omp_set_num_threads(use_threads);

        int n_total = L * L * L;
        size_t spin_memory = n_total * sizeof(int);
        size_t delta_memory = n_total * sizeof(int);
        size_t mag_memory = n_sample * sizeof(double);
        size_t seeds_memory = use_threads * sizeof(unsigned int);

        int n_den = static_cast<int>((den_start - den_end) / (-den_step)) + 1;
        size_t results_memory = n_den * sizeof(std::tuple<double, double, double, double>);
        size_t denominators_memory = n_den * sizeof(double);
        size_t betas_memory = n_den * sizeof(double);

        // 预估内存占用，防止超出上限
        double total_memory_bytes = static_cast<double>(spin_memory + delta_memory + mag_memory + seeds_memory + results_memory + denominators_memory + betas_memory);
        size_t total_memory = static_cast<size_t>(ceil(total_memory_bytes / (1024.0 * 1024.0)));

        if (total_memory > max_memory_mb) { std::cerr << "Error: Memory usage exceeds " << max_memory_mb << "MB limit" << std::endl; return EXIT_FAILURE; }

        std::mt19937::result_type seed_data = std::chrono::high_resolution_clock::now().time_since_epoch().count();
        std::random_device rd;
        for (int i = 0; i < 4; ++i) { seed_data ^= rd() << (i * 8); }
        std::mt19937 rng(seed_data);

        if (n_den <= 0) { std::cerr << "Error: Invalid number of density points." << std::endl; return EXIT_FAILURE; }

        std::vector<double> denominators;
        std::vector<double> betas;
        for (int i = 0; i < n_den; ++i) {
            double den = den_start + i * den_step;
            denominators.push_back(den);
            betas.push_back(1.0 / den);
        }
        int beta_count = betas.size();

        std::vector<int> spin(n_total);
        std::vector<std::tuple<double, double, double, double>> results;
        results.reserve(n_den);

        std::cout << "三维伊辛模型临界点模拟（" << L << "×" << L << "×" << L << "）" << std::endl;
        std::cout << "Beta序列：1/5.0, 1/4.9, ..., 1/4.0（共" << beta_count << "个点）" << std::endl;
        std::cout << "临界参考值：beta_c≈" << std::fixed << std::setprecision(4) << beta_c << "（对应分母≈" << std::fixed << std::setprecision(4) << den_c << "）" << std::endl;
        std::cout << "--------------------------------------------------------------------------------" << std::endl;
        std::cout << "使用线程数：" << use_threads << std::endl;
        std::cout << "内存占用预估：" << total_memory << "MB" << std::endl;
        std::cout << "--------------------------------------------------------------------------------" << std::endl;

        // 遍历不同密度值，逐点执行模拟
        for (int idx = 0; idx < beta_count; ++idx) {
            init_spin(spin, rng, idx);
            double den = denominators[idx];
            double beta = betas[idx];
            double rel_diff = std::abs((den - den_c) / den_c);

            std::cout << "\n正在处理分母=" << std::fixed << std::setprecision(1) << den << "（beta=" << std::fixed << std::setprecision(4) << beta << "）：第" << idx + 1 << "/" << beta_count << "个（高温→低温）" << std::endl;
            if (rel_diff < 0.05 / den_c) { std::cout << "  【临界点附近】den≈" << std::fixed << std::setprecision(4) << den_c << "，beta≈" << std::fixed << std::setprecision(4) << beta_c << std::endl; }

            // 计时并执行Metropolis核心模拟
            auto start = std::chrono::high_resolution_clock::now();
            double final_mag = ising_3d_metropolis(beta, rng, spin, idx);
            auto end = std::chrono::high_resolution_clock::now();

            std::chrono::duration<double> duration = end - start;
            double run_time = duration.count();

            results.emplace_back(den, beta, final_mag, run_time);
            std::cout << "  迭代完成！运行时间：" << std::fixed << std::setprecision(2) << run_time << " 秒" << std::endl;
            std::cout << "  " << ((rel_diff < critical_window) ? n_steps_critical : n_steps_base) << "步后的最终绝对序参量：" << std::fixed << std::setprecision(6) << final_mag << std::endl;
        }

        // 汇总输出所有模拟结果
        std::cout << "\n--------------------------------------------------------------------------------" << std::endl;
        std::cout << "所有beta值模拟完成！汇总结果（分母从5.0→4.0）：" << std::endl;
        std::cout << "--------------------------------------------------------------------------------" << std::endl;
        std::cout << std::left << std::setw(12) << "分母" << std::setw(10) << "beta"
                  << std::setw(15) << "绝对序参量" << std::setw(10) << "运行时间(s)" << std::endl;
        std::cout << "--------------------------------------------------------------------------------" << std::endl;

        for (const auto& res : results) {
            double den = std::get<0>(res);
            double beta = std::get<1>(res);
            double abs_mag = std::get<2>(res);
            double run_time = std::get<3>(res);
            std::cout << std::left << std::setw(12) << std::fixed << std::setprecision(1) << den
                      << std::setw(10) << std::fixed << std::setprecision(4) << beta
                      << std::setw(15) << std::fixed << std::setprecision(6) << abs_mag
                      << std::setw(10) << std::fixed << std::setprecision(2) << run_time
                      << std::endl;
        }

        std::cout << "\n注：临界参考值beta_c≈" << std::fixed << std::setprecision(4) << beta_c << "（分母≈" << std::fixed << std::setprecision(4) << den_c << "）" << std::endl;
        std::cout << "感谢使用！" << std::endl;
    } catch (const std::bad_alloc& e) {
        std::cerr << "Memory allocation failed: " << e.what() << std::endl;
        return EXIT_FAILURE;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    return 0;
}
