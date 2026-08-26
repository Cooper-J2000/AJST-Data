J/MNRAS/492/1919  Type I GRBs and the new classification method  (Minaev+, 2020)
================================================================================
The E_p,i_-E_iso_ correlation: type I gamma-ray bursts and the new
classification method.
    Minaev P.Y., Pozanenko A.S.
   <Mon. Not. R. Astron. Soc., 492, 1919-1936 (2020)>
   =2020MNRAS.492.1919M    (SIMBAD/NED BibCode)
================================================================================
ADC_Keywords: GRB ; Redshifts ; Gamma rays
Keywords: methods: data analysis - methods: statistical - catalogues -
          gamma-ray bursts - neutron star mergers - transients: supernovae

Abstract:
    We present the most extensive sample of 45 type I (short) and 275 type
    II (long) gamma-ray bursts (GRBs) with known redshift to investigate
    the correlation between the rest-frame peak energy, E_p,i_ and the
    total isotropic equivalent energy, E_iso_ of the prompt emission
    (Amati relation). The E_p,i_-E_iso_ correlation for type I bursts is
    found to be well distinguished from the one constructed for type II
    bursts and has a similar power-law index value,
    E_p,i_{prop.to}E_iso_^0.4^, which possibly indicates the same emission
    mechanism of both GRB types. We show that the initial pulse complex
    (IPC) of type I bursts with an extended emission and regular type I
    bursts follow the same correlation. We obtain similar results for type
    II bursts associated with Ic supernovae and for regular type II
    bursts. Three possible outliers from the E_p,i_-E_iso_ correlation for
    type II subsample are detected. Significant evolution of the
    E_p,i_-E_iso_ correlation with redshift for type II bursts is not
    found. We suggest the new classification method, based on the
    E_p,i_-E_iso_ correlation and introduce two parameters,
    EH=E_p,i,2_E_iso,51_^-0.4^ and EHD=E_p,i,2_
    E_iso,51_^-0.4^T_90,i_^-0.5^, where E_p,i,2_ is the value of E_p,i_
    parameter in units of 100keV, E_iso,51_ is the value of E_iso_
    parameter in units of 10^51^erg, and T_90,i_ is the rest-frame
    duration in units of seconds. EHD is found to be the most reliable
    parameter for the blind type I/type II classification, which can be
    used to classify GRBs with no redshift.

Description:
    To construct the sample of GRBs with a measured redshift (both
    spectroscopic and photometric) and E_p_ parameters we used different
    sources: GRB catalogues of Konus/Wind (Svinkin et al.
    2016ApJS..224...10S, Cat. J/ApJS/224/10; Tsvetkova et al.
    2017ApJ...850..161T, Cat. J/ApJ/850/161), BeppoSAX (Frontera et al.
    2009ApJS..180..192F, Cat. J/ApJS/180/192), and GBM/Fermi (Narayana
    Bhat et al. 2016ApJS..223...28N) experiments ; Papers concerning
    E_p,i_-E_iso_ correlation investigation (e.g. Amati
    2006MNRAS.372..233A; Qin & Chen 2013MNRAS.430..163Q; Zhang et al.
    2018PASP..130e4202Z; Zou et al. 2018ApJ...852L...1Z); Papers
    concerning analysis of individual GRBs (e.g. Minaev & Pozanenko
    2017AstL...43....1M; Pozanenko et al. 2018ApJ...852L..30P; Pandey et
    al. 2019MNRAS.485.5294P); GCN circulars archive
    (https://gcn.gsfc.nasa.gov/gcn3_archive.html); Online catalogue of
    well-localized GRBs by J. Greiner. (http://www.mpe.mpg.de/
    jcg/grbgen.html); The catalogue of GRB associated supernova (Cano et
    al. 2017AdAst2017E...5C); The paper related to the extended emission
    investigation of type I GRBs (Norris et al. 2010ApJ...717..411N).

    We also derive E_iso_ and E_p,i_ values for 45 GRBs using spectral
    parameters and redshift, available in the literature.

    The complete sample of GRBs including 45 type I and 275 type II bursts
    registered up to 2019, January is presented in Table A1.

File Summary:
--------------------------------------------------------------------------------
 FileName      Lrecl  Records   Explanations
--------------------------------------------------------------------------------
ReadMe            80        .   This file
tablea1.dat      152      320   The sample of gamma-ray bursts
refs.dat          87      130   References for Table A1
--------------------------------------------------------------------------------

See also:
  J/ApJS/224/10  : The second Konus-Wind short GRB catalog (Svinkin+, 2016)
  J/ApJ/850/161  : Konus-Wind cat. of GRBs with redshifts. I. (Tsvetkova+, 2017)
  J/ApJS/180/192 : BeppoSAX/GRBM {gamma}-ray Burst Catalog (Frontera+, 2009)

Byte-by-byte Description of file: tablea1.dat
--------------------------------------------------------------------------------
   Bytes Format Units     Label     Explanations
--------------------------------------------------------------------------------
   1-  7  A7    ---       GRB       GRB name (YYMMDDA)
       9  A1    ---     f_GRB       [*] Flag on GRB (1)
  11- 17  F7.2  s         T90i      Rest-frame duration of the burst (2)
  19- 25  F7.5  ---       z         Redshift
  27- 30  F4.2  ---     E_z         ? Upper error on z
  32- 35  F4.2  ---     e_z         ? Lower error on z
  37- 38  A2    ---     f_z         [PH ] Flag on z indicating the redshift is
                                     photometric
  40- 50  F11.6 10+44J    Eiso      Total isotropic equivalent energy
  52- 61  F10.6 10+44J  E_Eiso      Upper error on Eiso
  63- 72  F10.6 10+44J  e_Eiso      Lower error on Eiso
  74- 80  F7.2  keV       Epi       Rest-frame peak energy
  82- 89  F8.2  keV     E_Epi       Upper error on Epi
  91- 97  F7.2  keV     e_Epi       Lower error on Epi
  99-105  A7    ---       Type      Classification of the burst (3)
 107-116  A10   ---       Exp       Experiment used for the calculation on
                                     T_90,i_, E_p,i_ and E_iso_ values
 118-132  A15   ---       Ref       References
 134-138  F5.2  ---       EH        Energy-hardness parameter (EH) (4)
 140-141  A2    ---       EHtype    GRB type corresponding to the EH parameter
 143-149  F7.3  ---       EHD       Energy-Hardness-Duration parameter (EHD) (5)
 151-152  A2    ---       EHDtype   GRB type corresponding to the EHD parameter
--------------------------------------------------------------------------------
Note (1): Flag as follows:
    * = E_iso_ and E_p,i_ values por this source are calculated in the paper
Note (2): For the 'I+EE' GRBs the duration of the initial pulse complex (IPC) is
          given
Note (3): Type as follows:
  I       = Regular type I GRB (34/320)
  I+EE    = Type I GRB with an extended emission (11/320)
  II      = Regular type II GRB (235/320)
  II+SNph = Type II GRB with spectroscopically confirmed Ic supernova (19/320)
  II+SNsp = Type II GRB with photometrically confirmed Ic supernova (21/320)
Note (4): EH=(E_p,i_/100keV)/[(E_iso_/10^51^erg)^0.4^]
Note (5): EHD=EH/[(T_90,i_/1s)^0.5^]
--------------------------------------------------------------------------------

Byte-by-byte Description of file: refs.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label     Explanations
--------------------------------------------------------------------------------
   1-  3  I3    ---     Ref       [1/131] Reference number
   5- 23  A19   ---     BibCode   BibCode
  25- 67  A43   ---     Aut       Author's name
  69- 87  A19   ---     Com       Comments
--------------------------------------------------------------------------------

History:
    From electronic version of the journal

================================================================================
(End)                                           Ana Fiallos [CDS]    16-Mar-2023
