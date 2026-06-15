import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import numpy

def exp1figure():
    dc_base = 146500e-12
    dc_step = 10000e-12
    dc_values = np.array([dc_base + dc_step * i for i in range(60)])
    dc_nano = dc_values * 1e9

    freqs_raw = [
        None, None,
        116.99, 128.82, 140.09, 149.00, 166.68, 176.18, 184.81, 192.68,
        200.67, 209.33, 217.29, 220.43, 216.62, 223.13, 226.35, 238.00, 245.75, 251.55,
        261.84, 273.68, 274.33, 281.64, 290.90, 301.15, 301.43, 319.57, 320.22, 327.80,
        332.41, 339.68, 345.87, 351.22, 357.34, 362.47, 369.96, 376.22, 389.79, 395.62,
        400.91, 427.91, 433.06, 439.22, 451.54, 457.85, 462.28, 469.69, 477.30, 482.89,
        488.41, 494.45, 499.93, 506.49, 510.99, 522.70, 542.92, 578.70, 611.81, 617.95
    ]

    spiking_mask = np.array([f is not None for f in freqs_raw])
    spiking_dc = dc_nano[spiking_mask]
    spiking_freq = np.array([f for f in freqs_raw if f is not None])
    no_spike_dc = dc_nano[~spiking_mask]

    linear_end_idx = len(spiking_dc)
    slope_lin, intercept_lin, r_lin, p_lin, _ = stats.linregress(
        spiking_dc[:linear_end_idx], spiking_freq[:linear_end_idx]
    )
    r2_lin = r_lin**2
    fit_linear = slope_lin * spiking_dc[:linear_end_idx] + intercept_lin
    residuals = spiking_freq[:linear_end_idx] - fit_linear

    print(f"Gain (slope):    {slope_lin:.4f} Hz/nA")
    print(f"R²:              {r2_lin:.4f}")
    print(f"p-value:         {p_lin:.2e}")
    print(f"Threshold DC:    ~{spiking_dc[0]:.1f} nA")
    print(f"Threshold freq:  ~{spiking_freq[0]:.1f} Hz")
    print(f"Residual std:    {np.std(residuals):.2f} Hz")
    print(f"Max residual:    {np.max(np.abs(residuals)):.2f} Hz")

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(spiking_dc, spiking_freq, 'o-', color='#378ADD', linewidth=1.8,
            markersize=4, label='Measured firing rate', zorder=3)
    ax.plot(spiking_dc[:linear_end_idx], fit_linear, '--', color='#D85A30', linewidth=2,
            label=f'Linear fit (R²={r2_lin:.3f}, gain={slope_lin:.2f} Hz/nA)')
    ax.fill_between(spiking_dc[:linear_end_idx],
                    fit_linear, spiking_freq[:linear_end_idx],
                    alpha=0.15, color='#D85A30', label='Residuals')
    ax.scatter(no_spike_dc, [0, 0], s=80, facecolors='none',
            edgecolors='gray', linewidths=2, zorder=5, label='No spike detected')

    ax.axvline(spiking_dc[0], color='gray', linestyle=':', linewidth=1.2, alpha=0.7)
    ax.text(spiking_dc[0] + 1, 15, f'Threshold ~{spiking_dc[0]:.0f} nA',
            fontsize=9, color='gray')

    dip_x = spiking_dc[12:15]
    dip_y = spiking_freq[12:15]
    ax.annotate('Non-monotonic\nregion', xy=(dip_x[1], dip_y[1]),
                xytext=(dip_x[1] - 60, dip_y[1] - 60),
                arrowprops=dict(arrowstyle='->', color='darkorange'),
                fontsize=9, color='darkorange')

    ax.set_xlabel('DC input current (nA)', fontsize=12)
    ax.set_ylabel('Firing rate (Hz)', fontsize=12)
    ax.set_title('F-I curve — Neuron 6', fontsize=13)
    ax.legend(fontsize=10)
    ax.set_ylim(-30, 680)
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    plt.savefig('fi_curve_neuron6.png', dpi=150, bbox_inches='tight')
    plt.show()

def exp2figure():
    NO_EXPERIMENTS = 60
    plt.figure(figsize=(12, 4))
    colors = plt.cm.tab10.colors  # up to 10 distinct colors

    for i in range(NO_EXPERIMENTS):
        try:
            data    = numpy.loadtxt(f"spike_data_scope_{i+1}.csv", delimiter=',', skiprows=1)
            time_ax = data[:, 0]
            voltage = data[:, 1]
            plt.plot(time_ax * 1000, voltage, color=colors[i % len(colors)], label=f"Experiment {i+1}", alpha=0.5)
        except FileNotFoundError:
            print(f"No data file for experiment {i+1}, skipping")

    plt.xlabel("Time (ms)")
    plt.ylabel("Voltage (V)")
    plt.title("Scope capture — All Experiments")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def exp2figure2():
    base_freq = 50
    input_freqs = np.array([base_freq + (i // 2) * 50 for i in range(60)])

    random_data = [
        (1, None), (3, 1.49), (5, 20.26), (7, 31.15), (9, 38.50),
        (11, 44.60), (13, 49.42), (15, 52.59), (17, 55.97), (19, 60.40),
        (21, 63.05), (23, 65.46), (25, 67.97), (27, 69.93), (29, 72.54),
        (31, 74.10), (33, 75.82), (35, 78.03), (37, 79.03), (39, 79.90),
        (41, 81.19), (43, 83.03), (45, 83.58), (47, 84.95), (49, 85.64),
        (51, 85.98), (53, 86.67), (55, 87.41), (57, 88.38), (59, 89.06),
    ]
    fixed_data = [
        (2, None), (4, None), (6, None), (8, 31.06), (10, 40.70),
        (12, 48.16), (14, 54.57), (16, 60.25), (18, 65.43), (20, 69.72),
        (22, 73.55), (24, 77.13), (26, 80.22), (28, 83.24), (30, 85.62),
        (32, 88.26), (34, 90.25), (36, 92.53), (38, 94.42), (40, 96.15),
        (42, 98.27), (44, 99.60), (46, 100.20), (48, 100.38), (50, 99.86),
        (52, 99.48), (54, 99.85), (56, 99.58), (58, 100.27), (60, 100.04),
    ]

    fixed_x  = np.array([input_freqs[exp-1] for exp, f in fixed_data  if f is not None])
    fixed_y  = np.array([f                  for exp, f in fixed_data  if f is not None])
    random_x = np.array([input_freqs[exp-1] for exp, f in random_data if f is not None])
    random_y = np.array([f                  for exp, f in random_data if f is not None])

    fixed_no_spike_x  = np.array([input_freqs[exp-1] for exp, f in fixed_data  if f is None])
    random_no_spike_x = np.array([input_freqs[exp-1] for exp, f in random_data if f is None])

    slope_f, intercept_f, r_f, _, _ = stats.linregress(fixed_x,  fixed_y)
    slope_r, intercept_r, r_r, _, _ = stats.linregress(random_x, random_y)

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(fixed_x, fixed_y, 'o-', color='#378ADD', linewidth=1.8,
            markersize=4, label='Fixed spiking', zorder=3)
    ax.plot(random_x, random_y, 'o-', color='#D85A30', linewidth=1.8,
            markersize=4, label='Random spiking', zorder=3)

    ax.scatter(fixed_no_spike_x,  np.zeros(len(fixed_no_spike_x)),  s=80,
               facecolors='none', edgecolors='#378ADD', linewidths=2, zorder=5)
    ax.scatter(random_no_spike_x, np.zeros(len(random_no_spike_x)), s=80,
               facecolors='none', edgecolors='#D85A30', linewidths=2, zorder=5)

    ax.set_xlabel('Input frequency (Hz)', fontsize=12)
    ax.set_ylabel('Firing rate (Hz)', fontsize=12)
    ax.set_title('Firing rate vs Input frequency — Fixed vs Random spiking', fontsize=13)
    ax.legend(fontsize=10)
    ax.set_ylim(-15, 120)
    ax.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig('firing_rate_fixed_vs_random.png', dpi=150, bbox_inches='tight')
    plt.show()

def exp2figureoverlaid():
    plt.figure(figsize=(12, 4))
    colors = ["red", "blue"]

    for i in range(60):
        try:
            data    = numpy.loadtxt(f"spike_data_scope_{i+1}.csv", delimiter=',', skiprows=1)
            time_ax = data[:, 0]
            voltage = data[:, 1]
            plt.plot(time_ax * 1000, voltage, color=colors[i % len(colors)], label=f"Experiment {i+1}", alpha=0.5)
        except FileNotFoundError:
            print(f"No data file for experiment {i+1}, skipping")

    plt.xlabel("Time (ms)")
    plt.ylabel("Voltage (V)")
    plt.title("Scope capture — All Experiments")
    plt.grid(True)
    plt.legend(handles=[plt.Line2D([0],[0],color='red',label='Random spiking'), plt.Line2D([0],[0],color='blue',label='Fixed spiking')])
    plt.tight_layout()
    plt.show()


def exp1figure2():

    dc_base = 10e-12
    dc_step = 500000e-12

    dc_values = np.array([dc_base + dc_step * i for i in range(10)])
    dc_nano = dc_values * 1e9

    freqs_raw = [
        None, 382.00, 833.30, 1136.16, 1408.56,
        1512.75, 1506.71, 1510.36, 1506.18, 1506.20
    ]

    # --- remove invalid entries (None / NaN-safe) ---
    dc_clean = []
    freq_clean = []

    for x, y in zip(dc_nano, freqs_raw):
        if y is not None:
            dc_clean.append(x)
            freq_clean.append(y)

    dc_clean = np.array(dc_clean)
    freq_clean = np.array(freq_clean)

    # --- plot ---
    plt.figure(figsize=(6,4))

    plt.scatter(dc_clean, freq_clean, label="Mean Firing Rates")
    plt.plot(dc_clean, freq_clean, linestyle='-', alpha=0.7)  # connecting line

    plt.xlabel("DC (nA)")
    plt.ylabel("Frequency (Hz)")
    plt.title("Frequency vs DC")
    plt.grid(True)
    plt.legend()

    plt.show()
    

def exp2figure():
    NO_EXPERIMENTS = 60
    plt.figure(figsize=(12, 4))
    colors = plt.cm.tab10.colors  # up to 10 distinct colors

    for i in range(NO_EXPERIMENTS):
        try:
            data    = numpy.loadtxt(f"spike_data_scope_{i+1}.csv", delimiter=',', skiprows=1)
            time_ax = data[:, 0]
            voltage = data[:, 1]
            plt.plot(time_ax * 1000, voltage, color=colors[i % len(colors)], label=f"Experiment {i+1}", alpha=0.5)
        except FileNotFoundError:
            print(f"No data file for experiment {i+1}, skipping")

    plt.xlabel("Time (ms)")
    plt.ylabel("Voltage (V)")
    plt.title("Scope capture — All Experiments")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

 # I is in nA, so R will be fitted in V/nA = GΩ
def lif_firing_rate(I, delta_abs, tau_m, R, v_th):
    numerator = R * I
    denominator = R * I - v_th
    # avoid log of negative or zero
    ratio = numerator / denominator
    ratio = np.clip(ratio, 1.001, np.inf)
    return 1.0 / (delta_abs + tau_m * np.log(ratio))

def exp1figureagainstlifmodel():
    dc_base = 146500e-12
    dc_step = 10000e-12
    dc_values = np.array([dc_base + dc_step * i for i in range(60)])
    dc_nano = dc_values * 1e9

    freqs_raw = [
        None, None,
        116.99, 128.82, 140.09, 149.00, 166.68, 176.18, 184.81, 192.68,
        200.67, 209.33, 217.29, 220.43, 216.62, 223.13, 226.35, 238.00, 245.75, 251.55,
        261.84, 273.68, 274.33, 281.64, 290.90, 301.15, 301.43, 319.57, 320.22, 327.80,
        332.41, 339.68, 345.87, 351.22, 357.34, 362.47, 369.96, 376.22, 389.79, 395.62,
        400.91, 427.91, 433.06, 439.22, 451.54, 457.85, 462.28, 469.69, 477.30, 482.89,
        488.41, 494.45, 499.93, 506.49, 510.99, 522.70, 542.92, 578.70, 611.81, 617.95
    ]

    spiking_mask = np.array([f is not None for f in freqs_raw])
    spiking_dc = dc_nano[spiking_mask]
    spiking_freq = np.array([f for f in freqs_raw if f is not None])

    # initial guesses
    # delta_abs: ~2ms, tau_m: ~10ms, R: small since I is in nA, v_th: ~0.5V
    p0 = [0.002, 0.010, 0.001, 0.1]
    bounds = ([0, 0, 0, 0], [0.1, 1.0, 10.0, 10.0])

    try:
        popt, pcov = curve_fit(lif_firing_rate, spiking_dc, spiking_freq,
                            p0=p0, bounds=bounds, maxfev=50000)
        delta_abs, tau_m, R, v_th = popt
        perr = np.sqrt(np.diag(pcov))

        print(f"Refractory period (Δ_abs): {delta_abs*1000:.3f} ± {perr[0]*1000:.3f} ms")
        print(f"Membrane time constant (τ_m): {tau_m*1000:.3f} ± {perr[1]*1000:.3f} ms")
        print(f"Membrane resistance (R): {R:.6f} ± {perr[2]:.6f} V/nA")
        print(f"Threshold voltage (v_th): {v_th:.4f} ± {perr[3]:.4f} V")

        lif_curve = lif_firing_rate(spiking_dc, *popt)

        ss_res = np.sum((spiking_freq - lif_curve)**2)
        ss_tot = np.sum((spiking_freq - np.mean(spiking_freq))**2)
        r2 = 1 - ss_res / ss_tot
        print(f"\nR² of LIF fit: {r2:.4f}")

        fig, ax = plt.subplots(figsize=(9, 5))

        ax.plot(spiking_dc, spiking_freq, 'o-', color='#378ADD', linewidth=1.8,
                markersize=4, label='Measured firing rate', zorder=3)
        ax.plot(spiking_dc, lif_curve, '--', color='#D85A30', linewidth=2,
                label=f'LIF model fit (R²={r2:.3f})')
        ax.fill_between(spiking_dc, spiking_freq, lif_curve,
                        alpha=0.15, color='#D85A30', label='Deviation from LIF')
        ax.scatter(dc_nano[~spiking_mask], [0, 0], s=80, facecolors='none',
                edgecolors='gray', linewidths=2, zorder=5, label='No spike detected')

        ax.axvline(spiking_dc[0], color='gray', linestyle=':', linewidth=1.2, alpha=0.7)
        ax.text(spiking_dc[0] + 1, 15, f'Threshold ~{spiking_dc[0]:.0f} nA',
                fontsize=9, color='gray')

        textstr = (f'$\\Delta_{{abs}}$ = {delta_abs*1000:.2f} ms\n'
                f'$\\tau_m$ = {tau_m*1000:.2f} ms\n'
                f'$R$ = {R:.4f} V/nA\n'
                f'$v_{{th}}$ = {v_th:.3f} V')
        ax.text(0.98, 0.05, textstr, transform=ax.transAxes, fontsize=9,
                verticalalignment='bottom', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        ax.set_xlabel('DC input current (nA)', fontsize=12)
        ax.set_ylabel('Firing rate (Hz)', fontsize=12)
        ax.set_title('F-I curve — Neuron 6 vs LIF model fit', fontsize=13)
        ax.legend(fontsize=10)
        ax.set_ylim(-30, 680)
        ax.grid(True, alpha=0.2)

        plt.tight_layout()
        plt.savefig('fi_curve_lif_fit.png', dpi=150, bbox_inches='tight')
        plt.show()

    except RuntimeError as e:
        print(f"Fit failed: {e}")
        print("Try adjusting p0 initial guesses")

# --- model ---
def lif_firing_rate(I, tau_m, I_th, delta_abs):
    """
    I in nA, tau_m and delta_abs in ms, I_th in nA.
    Returns firing rate in Hz.
    Only valid for I > I_th.
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        period = delta_abs + tau_m * np.log(I / (I - I_th))
    return 1000.0 / period  # ms -> Hz  (1/ms = 1000 Hz)

def lifmodelfigure():
    
    # --- your data ---
    # I_data: DC current in nA (x-axis of Fig 5.4)
    # f_data: firing rate in Hz (y-axis of Fig 5.4)
    # Load these from your Experiment 1.3 output files
    dc_base = 146500e-12
    dc_step = 10000e-12
    dc_values = np.array([dc_base + dc_step * i for i in range(60)]) * 1e9  # in nA
    freqs_raw = [
        None, None,
        116.99, 128.82, 140.09, 149.00, 166.68, 176.18, 184.81, 192.68,
        200.67, 209.33, 217.29, 220.43, 216.62, 223.13, 226.35, 238.00, 245.75, 251.55,
        261.84, 273.68, 274.33, 281.64, 290.90, 301.15, 301.43, 319.57, 320.22, 327.80,
        332.41, 339.68, 345.87, 351.22, 357.34, 362.47, 369.96, 376.22, 389.79, 395.62,
        400.91, 427.91, 433.06, 439.22, 451.54, 457.85, 462.28, 469.69, 477.30, 482.89,
        488.41, 494.45, 499.93, 506.49, 510.99, 522.70, 542.92, 578.70, 611.81, 617.95
    ]

    I_data = dc_values  # shape (N,)
    f_data = np.array(freqs_raw)  # shape (N,)

    # Drop the zero-firing-rate (sub-threshold / "no spike detected") points —
    # the model is only defined for I > I_th and these correspond to f=0,
    # which the model can't reproduce (it asymptotes to 0 only as I -> I_th+,
    # never reaches exactly 0). Fit only on points where spiking was detected.
    f_data = np.array([np.nan if x is None else x for x in freqs_raw], dtype=float)
    mask = ~np.isnan(f_data)
    I_fit = I_data[mask]
    f_fit = f_data[mask]

    # --- initial guesses (important for convergence) ---
    # tau_m: guess something small, e.g. 0.1 ms
    # I_th: from Exp 1.2, somewhere in [144.5, 145.5]
    # delta_abs: from Exp 1.4, f_max ~ 1.5 kHz -> delta_abs ~ 1/1.5kHz = 0.667 ms
    p0 = [0.1, 145.0, 0.667]

    # bounds: tau_m > 0, I_th > 0 and < min(I_fit), delta_abs > 0
    bounds = (
        [1e-6, 1e-3, 1e-6],          # lower bounds
        [10.0, I_fit.min()*0.999, 10.0]  # upper bounds (I_th must be < smallest measured current)
    )

    popt, pcov = curve_fit(lif_firing_rate, I_fit, f_fit, p0=p0, bounds=bounds, maxfev=10000)
    tau_m_fit, I_th_fit, delta_abs_fit = popt
    perr = np.sqrt(np.diag(pcov))  # 1-sigma uncertainties

    print(f"tau_m     = {tau_m_fit:.4f} ± {perr[0]:.4f} ms")
    print(f"I_th      = {I_th_fit:.3f} ± {perr[1]:.3f} nA   (cf. Exp 1.2: [144.5, 145.5] nA)")
    print(f"delta_abs = {delta_abs_fit:.4f} ± {perr[2]:.4f} ms")
    print(f"-> predicted f_max = 1/delta_abs = {1000/delta_abs_fit:.1f} Hz  (cf. Exp 1.4: ~1500 Hz)")

    # --- goodness of fit ---
    f_pred = lif_firing_rate(I_fit, *popt)
    ss_res = np.sum((f_fit - f_pred)**2)
    ss_tot = np.sum((f_fit - np.mean(f_fit))**2)
    r2 = 1 - ss_res/ss_tot
    print(f"R^2 (LIF fit) = {r2:.4f}   (cf. linear fit: 0.988)")

    # --- plot ---
    I_smooth = np.linspace(I_fit.min(), I_fit.max(), 500)
    f_smooth = lif_firing_rate(I_smooth, *popt)

    plt.figure(figsize=(8,5))
    plt.scatter(I_data, f_data, label="Measured", color='tab:blue')
    plt.plot(I_smooth, f_smooth, color='tab:red', label=f"LIF fit ($R^2$={r2:.3f})")
    plt.axvline(I_th_fit, color='gray', ls='--', alpha=0.6, label=f"$I_{{th}}$ fit = {I_th_fit:.1f} nA")
    plt.axvspan(144.5, 145.5, color='green', alpha=0.2, label="$I_{th}$ from Exp 1.2")
    plt.xlabel("DC input current (nA)")
    plt.ylabel("Firing rate (Hz)")
    plt.title("F-I curve — LIF nonlinear fit vs. data")
    plt.legend()
    plt.tight_layout()
    plt.savefig("lif_fit.png", dpi=150)
    plt.show()

def main():
    lifmodelfigure()

main()