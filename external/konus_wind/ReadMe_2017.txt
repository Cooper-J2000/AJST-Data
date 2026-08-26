J/ApJ/850/161   Konus-Wind cat. of GRBs with redshifts. I.   (Tsvetkova+, 2017)
================================================================================
The Konus-Wind catalog of gamma-ray bursts with known redshifts.
I. Bursts detected in the triggered mode.
    Tsvetkova A., Frederiks D., Golenetskii S., Lysenko A., Oleynik P.,
    Pal'shin V., Svinkin D., Ulanov M., Cline T., Hurley K., Aptekar R.
   <Astrophys. J., 850, 161 (2017)>
   =2017ApJ...850..161T
================================================================================
ADC_Keywords: GRB; Redshifts
Keywords: catalogs ; gamma-ray burst: general ; methods: data analysis

Abstract:
    In this catalog, we present the results of a systematic study of
    gamma-ray bursts (GRBs) with reliable redshift estimates detected in
    the triggered mode of the Konus-Wind (KW) experiment during the period
    from 1997 February to 2016 June. The sample consists of 150 GRBs
    (including 12 short/hard bursts) and represents the largest set of
    cosmological GRBs studied to date over a broad energy band. From the
    temporal and spectral analyses of the sample, we provide the burst
    durations, the spectral lags, the results of spectral fits with two
    model functions, the total energy fluences, and the peak energy
    fluxes. Based on the GRB redshifts, which span the range 0.1<=z<=5, we
    estimate the rest-frame, isotropic-equivalent energy, and peak
    luminosity. For 32 GRBs with reasonably constrained jet breaks, we
    provide the collimation- corrected values of the energetics. We
    consider the behavior of the rest-frame GRB parameters in the
    hardness-duration and hardness-intensity planes, and confirm the
    "Amati" and "Yonetoku" relations for Type II GRBs. The correction for
    the jet collimation does not improve these correlations for the KW
    sample. We discuss the influence of instrumental selection effects on
    the GRB parameter distributions and estimate the KW GRB detection
    horizon, which extends to z~16.6, stressing the importance of GRBs as
    probes of the early universe. Accounting for the instrumental bias, we
    estimate the KW GRB luminosity evolution, luminosity and
    isotropic-energy functions, and the evolution of the GRB formation
    rate, which are in general agreement with those obtained in previous
    studies.

Description:
    Here, we present a complete sample of 150 gamma-ray bursts (GRBs) with
    reliably measured redshifts that triggered the Konus-Wind (KW; 13keV
    to 10MeV range) from 1997 February to 2016 June.

    The KW bursts observed in the waiting mode will be presented in a
    forthcoming catalog (A. Tsvetkova et al. 2017, in preparation).

File Summary:
--------------------------------------------------------------------------------
 FileName    Lrecl  Records    Explanations
--------------------------------------------------------------------------------
ReadMe          80        .    This file
table1.dat      92      150    General information
table2.dat     145      150    Durations and spectral lags
table3.dat     127      513    Spectral parameters
table4.dat     178      150    Burst energetics
table5.dat      92       41    Collimation-corrected parameters
refs.dat       152      182    References
--------------------------------------------------------------------------------

See also:
 J/A+A/427/87   : List of GRBs (Gorosabel+, 2004)
 J/ApJ/609/935  : Gamma-ray burst formation rate (Yonetoku+, 2004)
 J/ApJS/175/179 : The BAT1 gamma-ray burst catalog (Sakamoto+, 2008)
 J/ApJS/180/192 : BeppoSAX/GRBM {gamma}-ray Burst Catalog (Frontera+, 2009)
 J/ApJ/701/824  : Afterglows of short and long-duration GRBs (Nysewander+, 2009)
 J/ApJ/704/1405 : Testing the E_peak_-E_iso_ relation for GRBs (Krimm+, 2009)
 J/A+A/535/A57  : g'r'i'z'JH light curves of GRB 091127 (Filgas+, 2011)
 J/ApJ/731/103  : Redshift catalog for Swift long GRBs (Xiao+, 2011)
 J/ApJS/195/2   : The second Swift BAT GRB catalog (BAT2) (Sakamoto+, 2011)
 J/ApJ/746/170  : Follow-up resources for high-redshift GRBs (Morgan+, 2012)
 J/ApJS/208/21  : The BATSE 5B GRB spectral catalog (Goldstein+, 2013)
 J/A+A/557/A100 : Fermi and Swift GRBs E_peak_-E_iso_ relation (Heussaff+, 2013)
 J/ApJS/207/38  : IPN localizations of Konus short GRBs (Pal'shin+, 2013)
 J/ApJS/207/39  : IPN supplement to the Fermi GBM (Hurley+, 2013)
 J/ApJS/209/20  : Swift GRB catalog with X-ray data (Grupe+, 2013)
 J/ApJ/778/128  : GRB-host galaxies photometry (Perley+, 2013)
 J/ApJS/211/13  : The second Fermi/GBM GRB catalog (4yr) (von Kienlin+, 2014)
 J/A+A/581/A125 : UV/Optical/NIR spectroscopy GRB hosts (Kruehler+, 2015)
 J/A+A/582/A111 : List of 389 GRBs (Li+, 2015)
 J/A+A/584/A48  : New redshifts of 357 GBBs (Horvath+, 2015)
 J/ApJ/806/52   : 8 Fermi GRB afterglows follow-up (Singer+, 2015)
 J/ApJ/807/76   : 373 GRBs between 0.008<z<6.7 (Li+, 2015)
 J/ApJ/811/93   : Fermi/GBM GRB minimum timescales (Golkhou+, 2015)
 J/ApJS/224/10  : The second Konus-Wind short GRB catalog (Svinkin+, 2016)
 J/ApJS/224/20  : 10yr of Swift/XRT obs. of GRBs (Yi+, 2016)

Byte-by-byte Description of file: table1.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label   Explanations
--------------------------------------------------------------------------------
   1-  3 A3     ---     ---     [GRB]
   4- 10 A7     ---     GRB     Gamma-ray burst identifier (YYMMDDA)
  12- 13 I2     h       Trig.h  Hour of KW trigger time
  15- 16 I2     min     Trig.m  Minute of KW trigger time
  18- 23 F6.3   s       Trig.s  Second of KW trigger time
  25- 26 I2     h       Geo.h   Hour of the geocenter time (1)
  28- 29 I2     min     Geo.m   Minute of the geocenter time (1)
  31- 36 F6.3   s       Geo.s   Second of the geocenter time (1)
  38- 39 A2     ---     Type    Burst classification (2)
  41- 54 A14    ---     Inst    Mission/instrument (3)
  56- 58 I3     ---   r_Inst    [1/158] Reference for Inst (see refs.dat file)
  60- 64 A5     ---     OObs    Other observations (4)
  66- 67 A2     ---     Det     KW triggered detector
  69- 73 F5.1   deg     Angle   [4.8/102.4] Incident angle between the GRB
                                 direction and the detector axis
  75- 81 F7.5   ---     z       [0.09/5] Redshift
      83 A1     ---   n_z       [sp] Redshift type (s: spectroscopic or
                                  p: photometric)
  85- 87 I3     ---   r_z       [2/159] Reference for z (see refs.dat file)
  89- 92 A4     ---   f_z       Flag(s) on z (5)
--------------------------------------------------------------------------------
Note (1): Corrected for the burst front propagation from Wind to the
          Earth center.
Note (2): Burst classification as follows:
   I = GRBs are the merger-origin, typically short/hard bursts;
  II = GRBs are the collapsar-origin, typically long/soft GRBs.
Note (3): That provided the most accurate GRB localization from
          prompt emission observations.
Note (4): Other instrument as follows:
   1 = CGRO-BATSE;
   2 = HETE-2;
   3 = BeppoSAX-GRBM;
   4 = Swift-BAT;
   5 = Fermi-GBM;
   6 = Fermi-LAT.
Note (5): Flag as follows:
   1 = "Dark" burst according to the classification presented in the
       redshift reference paper;
   2 = "Dark" burst according to Fynbo et al. (2009ApJS..185..526F);
   3 = Although this burst is referred to as GRB 020819 in all related GCN
       circulars and in some other publications, this is the second GRB
       observed by KW on 2002 August 19;
   4 = This burst was initially referred to as GRB 050820, but, after the
       detection of GRB 050820B on the same day, it was renamed to GRB 050820A;
   5 = The redshift at 95% confidence level is z=2.77^+0.15^_-0.20_;
   6 = Although GRB 060121 is a short-duration burst, it was classified as
       Type II (see e.g. Zhang+ (2009ApJ...703.1696Z) or
       Svinkin (2016, J/ApJS/224/10) for details);
   7 = The redshift study of GRB 060121 (de Ugarte Postigo+ 2006ApJ...648L..83D)
       revealed two probability peaks. The main one (with a 63% likelihood)
       places the burst at z=4.6+/-0.5. A secondary peak (with a 35%
       likelihood) would imply that the afterglow lies at z=1.7+/-0.4;
   8 = The type of GRB 060614 is uncertain: a SN-less, long-duration burst
       (Gehrels+ 2006Natur.444.1044G ; Gal-Yam+ 2006Natur.444.1053G ;
       Fynbo+ 2006Natur.444.1047F ; Della Valle+ 2006Natur.444.1050D) is
       suggested to be a Type I burst based on its host galaxy low specific
       star-forming rate (Zhang+ 2009ApJ...703.1696Z), while in the KW data this
       GRB was classified as a Type II burst based on duration and hardness only
       (see Svinkin+ 2016, J/ApJS/224/10 for details);
   9 = This burst is a short burst with extended emission (EE) according to
       Sakamoto+ (2011, J/ApJS/195/2) and Svinkin+ (2016, J/ApJS/224/10);
  10 = The 95% confidence redshift range is 1.37<z<2.20;
  11 = The redshift at the 2{sigma} confidence level is z=4.35+/-0.15;
  12 = A rather wide 95% confidence range 1.14<z<2.34 is reported
       for this estimate;
  13 = Since there is an ambiguity with the host galaxy identification, this
       redshift may not correspond to the burst. See text (Section 3)
       for details;
  14 = Although this GRB cannot be unambiguously assigned to the Type I
       population, we classify it as Type I. See text (Section 3) for details.
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table2.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label     Explanations
--------------------------------------------------------------------------------
   1-  3 A3     ---     ---       [GRB]
   4- 10 A7     ---     GRB       Gamma-ray burst identifier (YYMMDDA)
  12- 19 F8.3   s       t0        [-265.3/260.7] Start time of T100
  21- 27 F7.3   s       T100      [0.1/485] Total burst duration
  29- 36 F8.3   s       t5        [-241.7/188]? Start time of T90
  38- 43 F6.3   s     e_t5        [0/73]? The 1{sigma} uncertainty in t5
  45- 51 F7.3   s       T90       [0/441]? Time interval containing 5% - 95% of
                                    total burst fluence
  53- 58 F6.3   s     e_T90       [0/76.6]? The 1{sigma} uncertainty in T90
  60- 66 F7.3   s       t25       [-56/190.3]? Start time of T50
  68- 73 F6.3   s     e_t25       [0/39.2]? The 1{sigma} uncertainty in t25
  75- 81 F7.3   s       T50       [0/167.3]? Time interval containing 25%-75% of
                                    total burst fluence
  83- 88 F6.3   s     e_T50       [0/39.3]? The 1{sigma} uncertainty in T50
  90- 97 F8.5   s       tlagG2G1  [-0.2/2.5]? Spectral lag between G2 and G1 KW
                                    energy channels (6)
  99-106 F8.5   s     e_tlagG2G1  [0/1.2]? The 1{sigma} uncertainty in tlagG2G1
 108-115 F8.5   s       tlagG3G1  [0/5.2]? Spectral lag between G3 and G1 KW
                                    energy channels (6)
 117-124 F8.5   s     e_tlagG3G1  [0/1.1]? The 1{sigma} uncertainty in tlagG3G1
 126-133 F8.5   s       tlagG3G2  [-0.3/0.8]? Spectral lag between G3 and G2 KW
                                    energy channels (6)
 135-142 F8.5   s     e_tlagG3G2  [0/0.4]? The 1{sigma} uncertainty in tlagG3G2
 144-145 A2     ---     Comm      Additional comments (7)
--------------------------------------------------------------------------------
Note (6): A positive spectral lag corresponds to the delay of the
          softer emission.
Note (7):
    1 = This GRB overlaps a solar flare at ~T0 + 130s;
    2 = Since GRB 081203A was detected during the GRB 081203B data transmission,
        there are no light curve data available for this GRB. The T100
        duration was determined based on the spectral data with a coarse time
        resolution of ~8s. Accordingly, for this GRB, only the lower limits
        on F_p_ and L_iso_ can be estimated from the KW data;
    3 = Since the T100 duration of GRB 120624B exceeds the trigger time
        history length, all temporal parameters of this burst were determined
        based on the waiting mode time history, i.e. with a coarse time
        resolution of ~3s.
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table3.dat
--------------------------------------------------------------------------------
   Bytes Format Units      Label  Explanations
--------------------------------------------------------------------------------
   1-  3 A3     ---        ---    [GRB]
   4- 10 A7     ---        GRB    Gamma-ray burst identifier (YYMMDDA)
      12 A1     ---        SType  Spectrum type (1)
  14- 20 F7.3   s          tstart [-0.3/326.2] Spectrum start time;
                                   relative to T_0_
  22- 28 F7.3   s          DeltaT [0.06/371] Spectrum accumulation time
  30- 33 A4     ---        SMod   Spectral model ("CPL"=cutoff power-law,
                                   "Band"=Band et al. 1993ApJ...413..281B or
                                   "PL")
  35- 37 A3     ---      f_SMod   Flag on SMod (0: non-BEST model
                                   or 1: BEST model)
  39- 43 F5.2   ---        alpha  [-2/0.6] Low-energy photon index
  45- 48 F4.2   ---      e_alpha  [0.01/0.9] Lower 1{sigma} uncertainty in alpha
  50- 53 F4.2   ---      E_alpha  [0.01/2.3] Upper 1{sigma} uncertainty in alpha
      55 I1     ---      l_beta   [0/1]? Limit flag on beta (2)
  57- 61 F5.2   ---        beta   [-5/0]? High-energy photon index
  63- 66 F4.2   ---      e_beta   [0/8.2]? Lower 1{sigma} uncertainty in beta
  68- 71 F4.2   ---      E_beta   [0/1.5]? Upper 1{sigma} uncertainty in beta
  73- 76 I4     keV        Ep     [0/4787]? EFE spectrum peak energy
  78- 81 I4     keV      e_Ep     [0/1197]? Lower 1{sigma} uncertainty in Ep
  83- 85 I3     keV      E_Ep     [0/949]? Upper 1{sigma} uncertainty in Ep
  87- 92 F6.2   10-9W/m2   F      [0.07/749.8] Spectral model normalization
  94- 98 F5.2   10-9W/m2 e_F      [0.01/19.7] Lower 1{sigma} uncertainty in F
 100-104 F5.2   10-9W/m2 E_F      [0.01/19.7] Upper 1{sigma} uncertainty in F
 106-110 F5.1   ---        chi2   [0/800.3]? Chi-square statistic of the fit
 112-114 I3     ---        DoF    [0/103]? Number of degrees of freedom
     116 I1     ---      l_P      [0/1]? Limit flag on P (2)
 118-124 F7.4   ---        P      [0/1.0]? Null hypothesis probability 
                                   (no correlation exists)
     127 I1     ---        Comm   ? Comment on the fits (3)
--------------------------------------------------------------------------------
Note (1): Spectrum type as follows:
     i = the spectrum is time-integrated and is used to calculate the burst
         total energy fluence;
     p = the spectrum is measured near the maximum count rate and is used
         to calculate the burst energy peak flux.
Note (2): Limit flag as follows:
     0 = the best fit value;
     1 = the upper limit;
 Blank = inapplicable (there is no high-energy photon index in the model).
Note (3): Comment as follows:
     1 = 3-channel fit (see Section 4.2.2);
     2 = Modeling the 3-channel spectrum for the interval from T0-33.734 s
         to T0+5.296 s yields the CPL model parameters which are in agreement
         with the provided multichannel fit ones;
     3 = 3-channel fit (see Section 4.2.2);
     4 = The energy channels above 2 MeV are strongly affected by the high
         and variable solar particle background, the spectral fits were
         performed up to 2 MeV.
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table4.dat
--------------------------------------------------------------------------------
   Bytes Format Units      Label  Explanations
--------------------------------------------------------------------------------
   1-  3 A3     ---        ---    [GRB]
   4- 10 A7     ---        GRB    Gamma-ray burst identifier (YYMMDDA)
  12- 15 F4.2   ---        z      [0.1/5] Redshift
  17- 24 F8.3   10-9J/m2   S      [1.1/2863] Energy fluence; 1e-6 erg/s
  26- 31 F6.3   10-9J/m2 e_S      [0.05/30] Lower 1{sigma} uncertainty in S
  33- 38 F6.3   10-9J/m2 E_S      [0.06/30] Upper 1{sigma} uncertainty in S
  40- 46 F7.3   s          Tp1024 [-0.5/367.2] Start time of interval when PCR
                                   on 1024ms time scale reached
  48- 48 I1     ---      f_Tp1024 ? Flag on Tp1024 (8)
  50- 56 F7.3   10-9W/m2   Fp1024 [0.3/509] Peak energy flux from 1024ms
                                   time scale; 1e-6erg/cm2/s
  58- 63 F6.3   10-9W/m2 e_Fp1024 [0.04/11] Lower 1{sigma} uncertainty in Fp1024
  65- 70 F6.3   10-9W/m2 E_Fp1024 [0.06/11] Upper 1{sigma} uncertainty in Fp1024
  72- 78 F7.3   s          Tp64   [-0.5/367.2] Start time of interval when PCR
                                   on 64ms time scale reached
  80- 86 F7.3   10-9W/m2   Fp64   [0.3/902] Peak energy flux from 64ms
                                   time scale; 1e-6erg/cm2/s
  88- 93 F6.3   10-9W/m2 e_Fp64   [0.04/25] Lower 1{sigma} uncertainty in Fp64
  95-100 F6.3   10-9W/m2 E_Fp64   [0.05/25] Upper 1{sigma} uncertainty in Fp64
 102-108 F7.3   s          Tp64r  [-0.5/367.2] Start time of interval when PCR
                                   on 64ms(1+z) time scale reached
 110-116 F7.3   10-9W/m2   Fp64r  [0.3/871] Peak energy flux from 64ms(1+z)
                                   time scale; 1e-6erg/cm2/s
 118-123 F6.3   10-9W/m2 e_Fp64r  [0.04/24] Lower 1{sigma} uncertainty in Fp64r
 125-130 F6.3   10-9W/m2 E_Fp64r  [0.05/24] Upper 1{sigma} uncertainty in Fp64r
 132-140 F9.4   10+44J     Eiso   [0.04/5810] Isotropic energy release; 1e+51erg
 142-149 F8.4   10+44J   e_Eiso   [0.005/440] The 1{sigma} uncertainty in Eiso
 151-158 F8.3   10+44W     Liso   [0.2/4650] Peak isotropic luminosity;
                                   in 1e+51erg/s units
 160-166 F7.3   10+44W   e_Liso   [0.05/190] The 1{sigma} uncertainty in Liso
 168-172 F5.2   10-9W/m2   Flim   [0/25]? Bolometric energy flux corresponding
                                   to GRB detection threshold; 1e-6erg/cm2/s
 174-178 F5.2   ---        Zmax   [0/16.7]? KW GRB detection horizon
--------------------------------------------------------------------------------
Note (8):
    1 = Since the trigger mode light curve begins at T0-0.512s, the
        corresponding peak energy flux may be underestimated due to the
        absence of high-res data before T0-0.512s.
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table5.dat
--------------------------------------------------------------------------------
   Bytes Format Units    Label   Explanations
--------------------------------------------------------------------------------
   1-  3 A3     ---      ---     [GRB]
   4- 10 A7     ---      GRB     Gamma-ray burst identifier (YYMMDDA)
  12- 17 F6.3   d        tjet    [0.1/35] Jet break time
  19- 23 F5.3   d      e_tjet    [0/6]? Lower 1{sigma} uncertainty on tjet (1)
  25- 30 F6.3   d      E_tjet    [0/12]? Upper 1{sigma} uncertainty on tjet (1)
  32- 33 A2     ---      CBM     Circumburst medium (2)
  35- 41 A7     ---      Ref     Reference(s) to tjet and CBM;
                                  see refs.dat file (3)
  43- 47 F5.2   deg      theta   [1.8/25.6] Jet opening angle {theta}_jet_ (4)
  49- 52 F4.2   deg    e_theta   [0.05/4.2] The 1{sigma} uncertainty in theta
  54- 58 F5.2   10-3     Coll    [0.5/97.5] Collimation factor (4)
  60- 64 F5.2   10-3   e_Coll    [0.03/16] The 1{sigma} uncertainty in Coll
  66- 72 F7.2   10+42J   Egamma  [1.2/1234] Collimation-corrected energy release
                                  in 1e+49erg units
  74- 79 F6.2   10+42J e_Egamma  [0.1/189] The 1{sigma} uncertainty in Egamma
  81- 86 F6.2   10+42W   Lgamma  [0.4/550] Collimation-corrected peak
                                  luminosity; 1e+49erg/s
  88- 92 F5.2   10+42W e_Lgamma  [0.02/83] The 1{sigma} uncertainty in Lgamma
--------------------------------------------------------------------------------
Note (1): When no tjet uncertainty is available from the literature, we take
          the sample-mean ~0.2*tjet as a 1{sigma} tjet error for the
          calculations.
Note (2): Circumburst medium (CBM) as follows:
   HM = In the case of a CBM with constant number density n
   WM = In the case of a stellar-wind-like CBM with n(r){propto}r^-2^
          In cases where no preferred CBM density profile is available from
          the literature, we provide the estimates for both HM and WM.
          See section 4.3.3 for further explanations.
Note (3): In cases where two references are given, the first one corresponds
          to the jet break time estimate and the second one corresponds to
          the preferred CBM.
Note (4): Knowing tjet, one can estimate the collimation-corrected energy
          released in gamma-rays Egamma=Eiso(1-cos{theta}_jet_) and the
          collimation-corrected peak luminosity Lgamma=Liso(1-cos{theta}_jet_),
          where {theta}_jet_ is the jet opening angle and (1-cos{theta}_jet_)
          is the collimation factor. See section 4.3.3.
--------------------------------------------------------------------------------

Byte-by-byte Description of file: refs.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label    Explanations
--------------------------------------------------------------------------------
   1-  3 I3     ---     Ref      Reference code
   5- 23 A19    ---     BibCode  ADS bibcode of the reference
  25- 48 A24    ---     Auth     Author's name
  50-152 A103   ---     Comm     Comment
--------------------------------------------------------------------------------

History:
    From electronic version of the journal

================================================================================
(End)                    Prepared by [AAS], Emmanuelle Perret [CDS]  02-Jul-2018
