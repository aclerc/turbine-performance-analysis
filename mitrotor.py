import sys
import os

# Add the folder path (absolute or relative)
sys.path.append(r"C:\Users\lashe\packages\turbine-performance-analysis")

#import lidar, turbine

from itertools import product
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import polars as pl
from tqdm import tqdm

from MITRotor import BEM, IEA3_4MW

figdir = Path("fig")
figdir.mkdir(exist_ok=True, parents=True)

pitches = np.linspace(-4.0, 15.0, 30)
#tsrs = np.linspace(3.0, 15.0, 30)
tsrs = [12.8, 12.9, 13.0, 13.1, 13.2]

bem = BEM(rotor=IEA3_4MW())
YAW = 0.0


def generate(cache_fn: Path = None) -> pl.DataFrame:
    """
    Run BEM for various pitch angles and tip-speed-ratios to generate contour
    data.
    """
    
    params = list(product(pitches, tsrs))

    df_list = []
    for pitch, tsr in tqdm(params):
        sol = bem(np.deg2rad(pitch), tsr, YAW)
        df_list.append(pl.DataFrame({"pitch": pitch, "tsr": tsr, "Cp": sol.Cp(), "Ct": sol.Ct()}))

    df = pl.concat(df_list)
    return df


def plot(df_surface: pl.DataFrame):
    df_piv_Cp = df_surface.pivot(index="tsr", columns="pitch", values="Cp", aggregate_function=None)
    df_piv_Ct = df_surface.pivot(index="tsr", columns="pitch", values="Ct", aggregate_function=None)
    tsr = df_piv_Cp["tsr"].to_numpy()
    pitch = np.array(df_piv_Cp.columns[1:], dtype=float)
    Cp = df_piv_Cp.to_numpy()[:, 1:]
    Cp[Cp < 0.01] = 0.01
    Cp[np.isnan(Cp)] = 0.02
    Ct = df_piv_Ct.to_numpy()[:, 1:]
    Ct[np.isnan(Ct)] = 0.02
    Ct[Ct < 0.01] = 0.01

    fig, axes = plt.subplots(1, 2, figsize=(8, 3))
    plt.subplots_adjust(wspace=0.5)

    [ax.set_xlabel(r"Pitch, $\theta_p~$(deg) ") for ax in axes]
    [ax.set_ylabel(r"Tip Speed Ratio, $\lambda~$(-)") for ax in axes]

    ## Plot surfaces
    levels = np.arange(0, 0.60, 0.02)
    CF_Cp = axes[0].contourf(pitch, tsr, Cp, levels=levels, cmap="viridis")
    CS = axes[0].contour(pitch, tsr, Cp, levels=levels, colors="k", linewidths=0.8)
    axes[0].clabel(CS, inline=True, fontsize=10)

    levels = np.arange(0, 2, 0.1)
    CF_Ct = axes[1].contourf(pitch, tsr, Ct, levels=levels, cmap="plasma")
    CS = axes[1].contour(pitch, tsr, Ct, levels=levels, colors="k", linewidths=0.8)
    axes[1].clabel(CS, inline=True, fontsize=10)

    # Add colorbar
    cbar = plt.colorbar(CF_Cp, ax=axes[0], aspect=20)
    cbar.set_label(label=r"$C_P~$(-)")

    cbar = plt.colorbar(CF_Ct, ax=axes[1], aspect=20)
    cbar.set_label(label=r"$C_T~$(-)")

    # Save figure to file
    plt.savefig(figdir / "example_3_pitch_tsr_contour.png", dpi=500, bbox_inches="tight")

def find_optimum(df: pl.DataFrame):
    # Find row with maximum Cp
    iterate = 0
    while(True):
        max_row = df.sort("Cp", descending=True).row(iterate)
        print(f"MAX ROW {iterate}: {max_row[2]}")
        if not np.isnan(max_row[2]): 
            break
        iterate+=1

    pitch_opt, tsr_opt, Cp_opt, Ct_opt = max_row

    print("\nOptimal Operating Point:")
    print(f"Pitch angle (deg): {pitch_opt:.3f}")
    print(f"Tip-speed ratio:   {tsr_opt:.3f}")
    print(f"Cp (max):          {Cp_opt:.4f}")
    print(f"Ct:                {Ct_opt:.4f}")

    return pitch_opt, tsr_opt, Cp_opt, Ct_opt

if __name__ == "__main__":
    print("Generate BEM data. This may take a couple of minutes.")
    df = generate()
    find_optimum(df)
    print("Optimum")
    print(df)
    print("plotting contour.")
    plot(df)
    plt.show()