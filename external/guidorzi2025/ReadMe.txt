J/A+A/690/A261     GRB variability-luminosity relationship     (Guidorzi+, 2024)
================================================================================
New results on the gamma-ray burst variability-luminosity relationship.
   Guidorzi C., Maccary R., Tsvetkova A., Kobayashi S., Amati L., Bazzanini L.,
   Bulla M., Camisasca A. E., Ferro L., Frederiks D., Frontera F., Lysenko A.,
   Maistrello M., Ridnaia A., Svinkin D., Ulanov M.
   <Astron. Astrophys. 690, A261 (2024)>
   =2024A&A...690A.261G         (SIMBAD/NED BibCode)
================================================================================
ADC_Keywords: Gamma rays ; GRB
Keywords: methods: data analysis - methods: statistical -
          gamma-ray burst: general

Abstract:
    At the dawn of the gamma-ray burst (GRB) afterglow era, a Cepheid-like
    correlation was discovered between the time variability V and the
    isotropic-equivalent peak luminosity Liso of the prompt emission of
    about a dozen long GRBs with measured redshift available at that time.
    Soon afterwards, the correlation was confirmed in a sample of about 30
    GRBs, even though it was affected by significant scatter. Unlike the
    minimum variability timescale (MVT), V measures the relative power of
    short-to-intermediate timescales.

    We aim to test the correlation using about 200 long GRBs with
    spectroscopically measured redshift, detected by Swift, Fermi, and
    Konus/WIND, for which both observables can be accurately estimated.

    The variability for all selected GRBs was calculated according to the
    original definition using the 64 ms background subtracted light curves
    of Swift/BAT (Fermi/GBM) in the 15-150 (8-900)keV energy passband.
    Peak luminosities were either taken from the literature or derived
    from modelling broad-band spectra acquired with either Konus/WIND or
    Fermi/GBM.

    The statistical significance of the correlation has weakened to <~2%,
    mostly due to the appearance of a number of smooth and luminous GRBs
    that are characterised by a relatively small V. At odds with most long
    GRBs, three out of four long-duration merger candidates have high V
    and low L_iso_.

    The luminosity is more tightly connected with shortest timescales
    measured by MVT than the short to intermediate timescales measured by
    V.We discuss the implications for internal dissipation models and the
    role of the e photosphere.We identified a few smooth GRBs with a
    single broad pulse and low V that might have an external shock origin,
    in contrast with most GRBs. The combination of high variability
    (V>~0.1), low luminosity L_iso_<~10^51^erg/s, and short MVT (<~0.1s)
    could be a good indicator for a compact binary merger origin.

Description:
    We report in the tables the values of variability and peak luminosity
    for the merged sample of bursts with statistically significant
    measures of both quantities. Table 1 reports variability calculated
    assuming f=0.8,, while Table 3 reports the analogous information
    obtained with f=0.45. The last four entries of each Table are long
    duration merger candidates, which are treated apart in the analysis.

File Summary:
--------------------------------------------------------------------------------
 FileName      Lrecl  Records   Explanations
--------------------------------------------------------------------------------
ReadMe            80        .   This file
table1.dat        92      216   Variability-Luminosity of 216 GRBs (f=0.8)
table3.dat        92      188   Variability-Luminosity of 188 GRBs (f=0.45)
refs.dat          99       31   References
--------------------------------------------------------------------------------

Byte-by-byte Description of file: table1.dat table3.dat
--------------------------------------------------------------------------------
   Bytes Format Units     Label     Explanations
--------------------------------------------------------------------------------
   1-  7  A7    ---       GRB       GRB name
  10- 16  F7.5  ---       z         Redshift
  18- 24  F7.2  s         Tf        Duraton of the time interval collecting
                                     a fraction f of total net counts
  27- 32  F6.2  s       e_Tf        Error of Tf (1-sigma) (1)
  35- 39  F5.3  ---       Vf        Variability assuming f (1)
  41- 45  F5.3  ---     s_Vf        Error of Vf (1-sigma)
  47- 52  F6.3  ---       Vf05      [] Negative error corresponding to 5
                                     percentile of Vf confidence interval
  54- 58  F5.3  ---       Vf95      Positive error corresponding to 95
                                     percentile of Vf confidence interval
  62- 67  F6.3  [10-7W]   logLiso   logarithm of Liso expressed in erg/s
                                     (isotropic-equivalent peak luminosity)
  70- 74  F5.3  [10-7W] e_logLiso   Error on logLiso (1-sigma)
  78- 80  A3    ---       Det       Detector used to calculate Vf
  86- 87  I2    ---     r_logLiso   Reference for logLiso, in refs.dat file
  90- 92  I3    ---       Npeaks    Number of peaks (3)
--------------------------------------------------------------------------------
Note (1): f=0.8 for table1 and f=0.45 for table3.
Note (3): Number of peaks with S/N>5 taken from Guidorzi et al.
           (2024A&A...685A..34G) and Maccary et al. (2024A&A...688L...8M).
--------------------------------------------------------------------------------

Byte-by-byte Description of file: refs.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label     Explanations
--------------------------------------------------------------------------------
   1-  2  I2    ---     Ref       Reference code
   4- 22  A19   ---     BibCode   BibCode
  24- 40  A17   ---     Aut       Author's name
  42- 99  A58   ---     Com       Comments
--------------------------------------------------------------------------------

Acknowledgements:
    Cristiano Guidorzi, guidorzi(at)fe.infn.it

================================================================================
(End)                                        Patricia Vannier [CDS]  27-Sep-2024
