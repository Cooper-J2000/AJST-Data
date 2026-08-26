J/ApJ/908/83  Konus-Wind catalog of GRBs with redshifts. II.  (Tsvetkova+, 2021)
================================================================================
The Konus-Wind Catalog of Gamma-Ray Bursts with Known Redshifts.
II. Waiting-Mode Bursts Simultaneously Detected by Swift/BAT.
    Tsvetkova A., Frederiks D., Svinkin D., Aptekar R., Cline T.L.,
    Golenetskii S., Hurley K., Lysenko A., Ridnaia A., Ulanov M.
   <Astrophys. J., 908, 83 (2021)>
   =2021ApJ...908...83T
================================================================================
ADC_Keywords: Gamma-ray burst; Redshifts
Keywords: Catalogs ; Gamma-ray bursts ; Astronomy data analysis

Abstract:
    In the second part of The Konus-Wind Catalog of Gamma-Ray Bursts with
    Known Redshifts (the first part: Tsvetkova+, 2017, J/ApJ/850/161;
    T17), we present the results of a systematic study of gamma-ray bursts
    (GRBs) with reliable redshift estimates detected simultaneously by the
    Konus-Wind (KW) experiment (in the waiting mode) and by the Swift/BAT
    (BAT) telescope during the period from 2005 January to the end of
    2018. By taking advantage of the high sensitivity of BAT and the wide
    spectral band of KW, we were able to constrain the peak spectral
    energies, the broadband energy fluences, and the peak fluxes for the
    joint KW- BAT sample of 167 weak, relatively soft GRBs (including four
    short bursts). Based on the GRB redshifts, which span the range
    0.04<~z<~9.4, we estimate the rest frame, isotropic-equivalent energy,
    and peak luminosity. For 14 GRBs with reasonably constrained jet
    breaks, we provide the collimation-corrected values of the energetics.
    This work extends the sample of KW GRBs with known redshifts to 338
    GRBs, the largest set of cosmological GRBs studied to date over a
    broad energy band. With the full KW sample, accounting for the
    instrumental bias, we explore GRB rest-frame properties, including
    hardness-intensity correlations, GRB luminosity evolution, luminosity
    and isotropic-energy functions, and the evolution of the GRB formation
    rate, which we find to be in general agreement with those reported in
    T17 and other previous studies.

Description:
    Konus-Wind (KW) is a gamma-ray spectrometer designed to study temporal
    and spectral characteristics of Gamma-Ray Bursts (GRBs), solar flares
    (SFs), soft gamma repeaters, and other transient phenomena over a wide
    energy range from 13keV to 10MeV.

    The Burst Alert Telescope (Swift/BAT) is a highly sensitive, large
    field-of-view (FoV:1.4sr for >50% coded FoV and 2.2sr for >10% coded
    FoV), coded-aperture telescope that detects and localizes GRBs in real
    time. The BAT is composed of a detector plane that has 32768 CdZnTe
    (CZT) detectors, and a coded-aperture mask that has ~52000 lead tiles.
    The BAT energy range is 14-150keV for imaging.

File Summary:
--------------------------------------------------------------------------------
 FileName    Lrecl  Records  Explanations
--------------------------------------------------------------------------------
ReadMe          80        .  This file
table1.dat      65      167  Joint KW/Swift-BAT sample
table2.dat     111      365  Spectral parameters
table4.dat     158      167  Burst energetics
table5.dat      88       22  Collimation-corrected parameters
refs.dat        68      131  References used for table1
--------------------------------------------------------------------------------

See also:
 J/ApJ/609/935  : Gamma-ray burst formation rate (Yonetoku+, 2004)
 J/ApJS/175/179 : The BAT1 gamma-ray burst catalog (Sakamoto+, 2008)
 J/ApJ/720/1513 : The afterglows of Swift-era GRBs. I. (Kann+, 2010)
 J/ApJS/195/2   : The second Swift BAT GRB catalog (BAT2) (Sakamoto+, 2011)
 J/ApJ/778/128  : GRB-host galaxies photometry (Perley+, 2013)
 J/A+A/581/A125 : UV/Optical/NIR spectroscopy GRB hosts (Kruehler+, 2015)
 J/ApJ/829/7    : The 3rd Swift/BAT GRB catalog (past ~11yrs) (Lien+, 2016)
 J/ApJS/224/10  : The second Konus-Wind short GRB catalog (Svinkin+, 2016)
 J/ApJ/850/161  : Konus-Wind cat. of GRBs with redshifts. I. (Tsvetkova+, 2017)

Byte-by-byte Description of file: table1.dat
--------------------------------------------------------------------------------
 Bytes  Format Units   Label  Explanations
--------------------------------------------------------------------------------
  1- 10 A10    ---     ID     Burst identifier
 12- 17 I6     ---     NumID  [103780/871316] Swift/BAT GRB Trigger number
 19- 30 A12    ---     Time   Swift/BAT trigger time, UT hh:mm:ss
 32- 38 F7.5   ---     z      [0.03/9.38] Redshift
 40- 42 A3     ---   f_z      Type for z (1)
 44- 46 A3     ---   r_z      Reference code for z
     48 A1     ---     Com    Comment on the burst (2)
 50- 57 F8.3   s       t0     [-230/60] Start time of T100 relative to Trig
 59- 65 F7.3   s       T100   [0.83/445] Total burst duration
--------------------------------------------------------------------------------
Note (1): Types as follows:
    s = spectroscopic (153 occurrences)
    p = photometric (13 occurrences)
    s+p = both (1 occurrence)
Note (2): Comment as follows:
    1 = There are two sources located within the revised XRT error circle.
        Here we use the redshift of one of them as a proxy for GRB redshift.
        The other source, which is a factor of 2 fainter, is likely to reside
        at an even higher redshift.
    2 = No emission was detected at the wavelengths shorter than 7500 Angstroms.
        This flux 'decrement' may be associated with the IGM at z~5.2 but
        could also be associated with a significant reddening of the afterglow.
    3 = A weak absorption system identified at z=0.696 could also be produced
        by an intervening system and thus the strict redshift range for this
        GRB would be 0.696<z<2.2.
    4 = The object is well detected and presents a featureless continuum
        except for a weak double line at z=1.036. No other clear features
        are detected. Therefore, 1.036<z<2.7 is suggested as redshift
        range for this GRB.
    5 = Given the low S/N of the spectrum, this redshift measurement should
        be considered tentative.
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table2.dat
--------------------------------------------------------------------------------
 Bytes   Format Units       Label   Explanations
--------------------------------------------------------------------------------
   1- 10 A10    ---         ID     Burst identifier
  12- 12 A1     ---         Type   Spectral type (1)
  14- 21 F8.3   s           Tstart [-109/382] Spectrum start time relative to T0
  23- 29 F7.3   s           dT     [2.94/416] Spectrum accumulation time
  31- 34 A4     ---         Model  Spectral model used
  36- 40 F5.2   ---         Alpha  [-1.84/0.71] Low-energy photon index
  42- 45 F4.2   ---       e_Alpha  [0.04/2] Lower 1{sigma} uncertainty in Alpha
  47- 50 F4.2   ---       E_Alpha  [0.05/3] Upper 1{sigma} uncertainty in Alpha
  52- 56 F5.2   ---         Beta   [-3.46/-1.75]? High-energy photon index
  58- 61 F4.2   ---       e_Beta   [0.07/9]? Lower 1{sigma} uncertainty in Beta
  63- 66 F4.2   ---       E_Beta   [0.06/3]? Upper 1{sigma} uncertainty in Beta
  68- 70 I3     keV         Ep     [27/578] EFE spectrum peak energy
  72- 74 I3     keV       e_Ep     [2/293] Lower 1{sigma} uncertainty in Ep
  76- 79 I4     keV       E_Ep     [2/2803] Upper 1{sigma} uncertainty in Ep
  81- 84 F4.2   10-10W/m2   F      [0.1/8.66] Spectral model normalization flux
                                    (1e^-7^erg/s/cm^2^)
  86- 89 F4.2   10-10W/m2 e_F      [0.01/1.43] Lower 1{sigma} uncertainty in F
  91- 94 F4.2   10-10W/m2 E_F      [0.02/1.5] Upper 1{sigma} uncertainty in F
  96-100 F5.1   ---         Chi2   [34.3/103] Chi-square statistic of the fit
 102-103 I2     ---         DoF    [58/59] Number of degrees of freedom
 105-111 F7.5   ---         Prob   [0.0003/1] Null hypothesis probability
--------------------------------------------------------------------------------
Note (1): Types as follows:
    i = the spectrum is time-integrated and is used to calculate
        the burst total energy fluence (222 occurrences)
    p = the spectrum is measured near the maximum count rate and
        is used to calculate the burst energy peak flux (143 occurrences)
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table4.dat
--------------------------------------------------------------------------------
 Bytes   Format Units       Label  Explanations
--------------------------------------------------------------------------------
   1- 10 A10    ---         ID     Burst identifier
  12- 18 F7.5   ---         z      [0.03/9.38] Spectroscopic redshift
  20- 25 F6.2   10-10J/m2   S      [1.36/405] Energy fluence; 1e-7erg/s
  27- 32 F6.2   10-10J/m2 e_S      [0.2/70] Lower 1{sigma} uncertainty in S
  34- 38 F5.2   10-10J/m2 E_S      [0.2/89] Upper 1{sigma} uncertainty in S
  40- 46 F7.3   s           Tp1024 [0/390] Start time of interval when PCR on
                                    1024ms time scale reached (1)
  48- 52 F5.2   10-10W/m2   Fp1024 [0.52/10.2] Peak energy flux from 1024ms time
                                    scale (1e-7erg/cm^2^/s)
  54- 58 F5.2   10-10W/m2 e_Fp1024 [0.1/3] Lower 1{sigma} uncertainty in Fp1024
  60- 63 F4.2   10-10W/m2 E_Fp1024 [0.1/3] Upper 1{sigma} uncertainty in Fp1024
  65- 71 F7.3   s           Tp64   [0.008/396] Start time of interval when PCR
                                    on 64ms time scale reached (1)
  73- 77 F5.2   10-10W/m2   Fp64   [1.36/31.9] Peak energy flux from 64ms time
                                    scale (1e-7erg/cm^2^/s)
  79- 83 F5.2   10-10W/m2 e_Fp64   [0.3/10] Lower 1{sigma} uncertainty in Fp64
  85- 88 F4.2   10-10W/m2 E_Fp64   [0.4/9] Upper 1{sigma} uncertainty in Fp64
  90- 96 F7.3   s           Tp64r  [0.01/394] Start time of interval when PCR on
                                    64ms(1+z) time scale reached (1)
  98-102 F5.2   10-10W/m2   Fp63r  [0.75/28.7] Peak energy flux from 64ms(1+z)
                                    time scale (1e-7erg/cm^2^/s)
 104-108 F5.2   10-10W/m2 e_Fp63r  [0.2/9] Lower 1{sigma} uncertainty in Fp64r
 110-113 F4.2   10-10W/m2 E_Fp63r  [0.3/8] Upper 1{sigma} uncertainty in Fp64r
 115-121 F7.2   10+44J      Eiso   [0.03/1477] Isotropic energy release 1e+51erg
 123-129 F7.2   10+44J    e_Eiso   [0/255] Lower 1{sigma} uncertainty in Eiso
 131-136 F6.2   10+44J    E_Eiso   [0/326] Upper 1{sigma} uncertainty in Eiso
 138-143 F6.2   10+44W      Liso   [0/514] Peak isotropic luminosity; 1e+51erg/s
 145-151 F7.2   10+44W    e_Liso   [0/131] Lower 1{sigma} uncertainty in Liso
 153-158 F6.2   10+44W    E_Liso   [0/104] Upper 1{sigma} uncertainty in Liso
--------------------------------------------------------------------------------
Note (1): Relative to BAT trigger time.
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table5.dat
--------------------------------------------------------------------------------
 Bytes  Format Units    Label  Explanations
--------------------------------------------------------------------------------
  1- 10 A10    ---      ID     Burst identifier
 12- 15 F4.2   d        tJet   [0.03/9.49]? Jet break time
 17- 21 F5.2   d      e_tJet   [0.01/1]? Uncertainty in tJet
 23- 25 A3     ---      CBM    Circumburst medium (1)
 27- 29 A3     ---      Ref    Reference code for tJet and CBM (2)
 31- 35 F5.2   deg      theta  [1.26/10.2] Jet opening angle
 37- 40 F4.2   deg    e_theta  [0.04/0.6] Uncertainty in theta
 42- 46 F5.2   10-3     Col    [0.24/15.8] Collimation factor
 48- 51 F4.2   10-3   e_Col    [0.03/0.9] Uncertainty in Col
 53- 58 F6.2   10+42J   Egamma [0.59/233] Collimation-corrected energy release;
                                1e+49erg
 60- 65 F6.2   10+42J e_Egamma [0.1/56] Lower 1{sigma} uncertainty in Egamma
 67- 71 F5.2   10+42J E_Egamma [0.1/57] Upper 1{sigma} uncertainty in Egamma
 73- 77 F5.2   10+42W   Lgamma [0.43/29.1] Collimation-corrected peak luminosity
                                1e+49 erg/s
 79- 83 F5.2   10+42W e_Lgamma [0.1/8] Lower 1{sigma} uncertainty in Lgamma
 85- 88 F4.2   10+42W E_Lgamma [0.1/9] Upper 1{sigma} uncertainty in Lgamma
--------------------------------------------------------------------------------
Note (1): In cases where the preferred CBM density profile is known, it is
          taken from the same paper as tjet. Otherwise, calculations for both
          CBMs are provided and the geometric mean of the HM and WM energetics
          is used in the calculations.
Note (2): References as follows:
    (1) = Ghirlanda+, 2007A&A...466..127G
    (2) = Afonso+, 2011A&A...526A.154A
    (3) = Wang+, 2018ApJ...859..160W
    (4) = Kann+, 2010, J/ApJ/720/1513
    (5) = Frail+, 2006ApJ...646L..99F
--------------------------------------------------------------------------------

Byte-by-byte Description of file: refs.dat
--------------------------------------------------------------------------------
  Bytes  Format Units   Label     Explanations
--------------------------------------------------------------------------------
  1-  3  I3     ---     Ref       [1/131] Reference code
  5- 33  A29    ---     Autor     Main autor for the reference
 35- 53  A19    ---     BIB       BIBcode
 55- 68  A14    ---     Cat.      Vizier catalog
--------------------------------------------------------------------------------

History:
    From electronic version of the journal

References:
    Tsvetkova et al.     Paper I : 2017ApJ...850..161T    Cat. J/ApJ/850/161

================================================================================
(End)                          Prepared by [AAS], Coralie Fix [CDS], 04-Jul-2022
