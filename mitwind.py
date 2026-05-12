from mitwindfarm import Area, AD, UnifiedAD, BEM, GaussianWakeModel, VariableKwGaussianWakeModel
from mitwindfarm import Uniform, PowerLaw, Niayifar, Layout, GridLayout, Windfarm, Plotting, WindfarmSolution
from MITRotor.ReferenceTurbines import IEA3_4MW, IEA15MW
from MITRotor.Momentum import UnifiedMomentum
from MITRotor.TipLoss import PrandtlTipLoss
from pathlib import Path
from scipy.optimize import minimize
from rich import print
import numpy as np
import matplotlib.pyplot as plt
import MITRotor as mr
from numpy.typing import ArrayLike
from mitwindfarm.Windfield import Windfield

class myWindField(Windfield):
    """
    Concrete implementation of a power law wind field.

    Methods:
    - shear(y): Returns the wind speed due to shear
    - wsp(x, y, z): Returns wind speed at a given height z
    - TI(x, y, z): Returns the input turbulence intensity TIamb with the same shape as input coordinates.
    - wdir(x, y, z): Returns an array of zeros with the same shape as input coordinates.
    """
    def __init__(self, Uref: float, zref: float, exp: float, TIamb: float = 0.0, wind_direction=np.pi):
        self.Uref = Uref
        self.zref = zref
        self.exp = exp
        self.TIamb = TIamb
        self.wind_direction = wind_direction

    def shear(self, y):
        """
        Returns wind speed due to shear.
        """
        u = self.Uref * (y / self.zref) ** self.exp
        u = np.nan_to_num(u)
        return u

    def wsp(self, x: ArrayLike, y: ArrayLike, z: ArrayLike) -> ArrayLike:
        u = self.Uref * (z / self.zref) ** self.exp
        u = np.nan_to_num(u)
        return u
    
    def TI(self, x: ArrayLike, y: ArrayLike, z: ArrayLike) -> ArrayLike:
        return self.TIamb * np.ones_like(x)

    def wdir(self, x: ArrayLike, y: ArrayLike, z: ArrayLike) -> ArrayLike:
        return np.full_like(x, np.pi) 

FIGDIR = Path(__file__).parent.parent / "fig"
FIGDIR.mkdir(exist_ok=True, parents=True)

uniform_wind_field = Uniform(U0=5)
rotor_bem = BEM(IEA3_4MW(), momentum_model=UnifiedMomentum())
rotor_bem2 = BEM(IEA3_4MW(), momentum_model=UnifiedMomentum(), tiploss_model=PrandtlTipLoss())
gaussian_wake_model = GaussianWakeModel()
niayifar_superposition = Niayifar()

windfarm_unified_bem = Windfarm(rotor_model = rotor_bem, wake_model = gaussian_wake_model, 
                                superposition = niayifar_superposition,
                                base_windfield = myWindField(Uref=5, zref=49, exp=0.2), TIamb = 0.0)

xs = [-7.025673286343040, -7.027825861471880, -7.031686473251470,
      -7.018845156557210, -7.023359900029670, -7.027901986951650,
      -7.031306770597570, -7.018780343888710, -7.021212846200650]
for element in range(0,9):
    xs[element] = xs[element]*111111/62
ys = [54.970666557294800, 54.968824310006900, 54.955039264508300, 54.960595588013500,
      54.963686168399900, 54.954038890673300, 54.952655740296500, 54.963254036914000, 
      54.958243159959000]
for element in range(0,9):
    ys[element] = ys[element]*64000/62

def make_windfarm(exes, whys, windfarm, show=True, savefig=False, ax=0, ylabel=''):
    layout = Layout(exes, whys)
    bem_setpoints = [(0,7,0,0) for i in range(0,9)]
    windfarm_solution = windfarm(layout, bem_setpoints)
    if ax==0: fig, ax=plt.subplots(figsize=(6,3))
    Plotting.plot_windfarm(windfarm_solution, ax)
    ax.set_ylabel(ylabel=ylabel, fontsize=12)
    ax.set_title("Altahullion Wind Farm", fontsize=20)
    if savefig: plt.savefig(savefig, bbox_inches='tight')
    if show: plt.show()

momentum_model= UnifiedMomentum(averaging = "rotor")
windfarm_unified_bem = Windfarm(
    rotor_model=BEM(IEA3_4MW(), momentum_model = momentum_model),
    TIamb=0.1,
)

make_windfarm(xs, ys, windfarm_unified_bem)

rotor_15mw = mr.IEA15MW()
rotor_10mw = mr.IEA10MW()
rotor_geometry = mr.BEMGeometry(Nr = 20, Ntheta = 30)
no_tip_loss = mr.NoTipLoss()
prandtl_tip_loss = mr.PrandtlTipLoss(root_loss = True)
unified_momentum_model = mr.UnifiedMomentum(averaging = "rotor")
tangential_induction_model = mr.DefaultTangentialInduction()
default_aerodynamic_model = mr.DefaultAerodynamics()
kragh_aerodynamic_model = mr.KraghAerodynamics()

bem_model = mr.BEM(
    rotor = rotor_10mw,
    geometry = rotor_geometry,
    tiploss_model = prandtl_tip_loss,
    momentum_model = unified_momentum_model,
    tangential_induction_model = tangential_induction_model,
    aerodynamic_model = kragh_aerodynamic_model
)

pitch, tsr, yaw = np.deg2rad(0), 7.0, np.deg2rad(20.0)
sol = bem_model(pitch, tsr, yaw)

# Print various quantities in BEM solution
if sol.converged:
    print(f"BEM solution converged in {sol.niter} iterations.")
else:
    print("BEM solution did NOT converge!")

print(f"Control setpoints: {sol.pitch=:2.2f}, {sol.tsr=:2.2f}, {sol.yaw=:2.2f}")
print(f"Power coefficient: {sol.Cp():2.2f}")
print(f"Thrust coefficient: {sol.Ct():2.2f}")
print(f"Local thrust coefficient: {sol.Ctprime():2.2f}")
print(f"Axial induction: {sol.a():2.2f}")
print(f"Rotor-effective windspeed: {sol.U():2.2f}")
print(f"Far-wake streamwise velocity: {sol.u4:2.2f}")
print(f"Far-wake lateral velocity: {sol.v4:2.2f}")