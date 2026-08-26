function localizedGRB (value) {
   for ( i=0; i < table.length ; i++ )  {
     if ( value=="ALL" ) { table[i].yn = 1; }
     else if ( value=="FULL" && table[i].MCAL == "Y") { table[i].yn = 1; } //Fully acquired (campo 11=Y - cioè MCAL - sono 393)
     else if ( value=="YES" && table[i].LOC !== "") { table[i].yn = 1; }
     else if ( value=="NO" && table[i].LOC == "") { table[i].yn = 1; }
     else { table[i].yn = 0; } 
   }
}

function rowField (p0,p1,p2) {
// parameters values for one column 
  this.p0 = p0
  this.p1 = p1
  this.p2 = p2
}

function catEntry(NAME,RA,Dec,l,b,T0,MET,Orbit,RM_SA,RM_AC,RM_MCAL,MCAL,BKG,T50,err_T50,BKGSUB_CTS_T50,T90,err_T90,BKGSUB_CTS_T90,LOC,THETA,PHI,PL_RANGE,PL_BETA,PL_BETA_emin,PL_BETA_emax,PL_RED_CHI_SQ,PL_DOF,PL_FLUX,PL_FLUENCE,BAND_RANGE,BAND_ALPHA,BAND_ALPHA_emin,BAND_ALPHA_emax,BAND_BETA,BAND_BETA_emin,BAND_BETA_emax,Ec,Ep,Eb,BAND_RED_CHI_SQ,BAND_DOF,BAND_FLUX,BAND_FLUENCE) {
  this.NAME = NAME;
  this.radeg = RA; //right ascension in degrees (J2000)
  if (this.radeg == "") { this.ra = this.radeg; } else { this.ra = chRA(this.radeg); } //right ascension in hh mm ss.ff
  this.decdeg = Dec; //declination in degrees (J2000)
  if (this.decdeg == "") { this.dec = this.decdeg; } else { this.dec = chDEC(this.decdeg); } //declination in dd mm ss.ff
  this.lii = l; 
  this.bii = b; 
  this.T0 = T0;
  this.MET = MET;
  this.Orbit = Orbit;
  this.RM_SA = RM_SA;
  this.RM_AC = RM_AC;
  this.RM_MCAL = RM_MCAL;
  this.MCAL = MCAL;
  this.BKG = BKG;
  this.T50 = T50;
  this.err_T50 = err_T50;
  this.BKGSUB_CTS_T50 = BKGSUB_CTS_T50;
  this.T90 = T90;
  this.err_T90 = err_T90;
  this.BKGSUB_CTS_T90 = BKGSUB_CTS_T90;
  this.LOC = LOC;
  this.THETA = THETA;
  this.PHI = PHI;
  this.PL_RANGE = PL_RANGE;
  this.PL_BETA = PL_BETA;
  this.PL_BETA_emin = PL_BETA_emin;
  this.PL_BETA_emax = PL_BETA_emax;
  this.PL_RED_CHI_SQ = PL_RED_CHI_SQ;
  this.PL_DOF = PL_DOF;
  this.PL_FLUX = PL_FLUX;
  this.PL_FLUENCE = PL_FLUENCE;
  this.BAND_RANGE = BAND_RANGE;
  this.BAND_ALPHA = BAND_ALPHA;
  this.BAND_ALPHA_emin = BAND_ALPHA_emin;
  this.BAND_ALPHA_emax = BAND_ALPHA_emax;
  this.BAND_BETA = BAND_BETA;
  this.BAND_BETA_emin = BAND_BETA_emin;
  this.BAND_BETA_emax = BAND_BETA_emax;
  this.Ec = Ec;
  this.Ep = Ep;
  this.Eb = Eb;
  this.BAND_RED_CHI_SQ = BAND_RED_CHI_SQ;
  this.BAND_DOF = BAND_DOF;
  this.BAND_FLUX = BAND_FLUX;
  this.BAND_FLUENCE = BAND_FLUENCE;
}

function tabRow(F0,F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11,F12,F13,F14,F15,F16,F17,F18,F19,F20,F21,F22,F23,F24,F25,F26,F27,F28,F29,F30,F31,F32,F33,F34,F35,F36,F37,F38,F39,F40,F41,F42){
  this.f = new Array;
  this.f[0]  =  F0;  this.f[1]  =  F1;  this.f[2]  =  F2;  this.f[3]  =  F3;  this.f[4]  =  F4;
  this.f[5]  =  F5;  this.f[6]  =  F6;  this.f[7]  =  F7;  this.f[8]  =  F8;  this.f[9]  =  F9;
  this.f[10] = F10;  this.f[11] = F11;  this.f[12] = F12;  this.f[13] = F13;  this.f[14] = F14;
  this.f[15] = F15;  this.f[16] = F16;  this.f[17] = F17;  this.f[18] = F18;  this.f[19] = F19;
  this.f[20] = F20;  this.f[21] = F21;  this.f[22] = F22;  this.f[23] = F23;  this.f[24] = F24;
  this.f[25] = F25;  this.f[26] = F26;  this.f[27] = F27;  this.f[28] = F28;  this.f[29] = F29;
  this.f[30] = F30;  this.f[31] = F31;  this.f[32] = F32;  this.f[33] = F33;  this.f[34] = F34;
  this.f[35] = F35;  this.f[36] = F36;  this.f[37] = F37;  this.f[38] = F38;  this.f[39] = F39;
  this.f[40] = F40;  this.f[41] = F41;  this.f[42] = F42;
}

// load default options and lables for each column in table 
//,undefined,undefined,undefined,undefined,'COMMENT'
Ihf0  = new fld('NAME','0','-','-','-','NAME',undefined,undefined,undefined,undefined,'GRB name');
Ihf1  = new fld('RA (J2000)','0','hh mm ss.d','degrees','-',undefined,undefined,undefined,undefined,undefined,'Right Ascension (J2000) in hh.mm.ss.d or degrees');
Ihf2  = new fld('Dec (J2000)','0','dd mm ss.d','degrees','-',undefined,undefined,undefined,undefined,undefined,'Declination (J2000) in dd.mm.ss.d or degrees');
Ihf3 = new fld ('l<br>(deg)','h','-','-','-','lii',undefined,undefined,undefined,undefined,'Galactic longitude, in degrees'); 
Ihf4 = new fld ('b<br>(deg)','h','-','-','-','bii',undefined,undefined,undefined,undefined,'Galactic latitude, in degrees'); 
Ihf5  = new fld('Trigger&nbsp;Time&nbsp;(T0)','0','UTC','MET','-',undefined,undefined,undefined,undefined,undefined,'Trigger time in UTC, in the form YYYY-MM-DDThh:mm:ss or AGILE MET in s');
Ihf6  = new fld('Orbit','0','-','-','-','Orbit',undefined,undefined,undefined,undefined,'AGILE orbit number');
Ihf7  = new fld('RM_SA flag','h','-','-','-','RM_SA',undefined,undefined,undefined,undefined,'Type of SA ratemeter detection');
Ihf8  = new fld('RM_AC flag','h','-','-','-','RM_AC',undefined,undefined,undefined,undefined,'Type of AC ratemeter detection');
Ihf9  = new fld('RM_MCAL flag','h','-','-','-','RM_MCAL',undefined,undefined,undefined,undefined,'Type of MCAL ratemeter detection');
Ihf10 = new fld('MCAL flag','0','-','-','-','MCAL',undefined,undefined,undefined,undefined,'Type of detection in MCAL: Y=complete, I=incomplete, F=fragmented, N=no detection, n=no data.');
Ihf11 = new fld('BKG<br>(Hz)','h','-','-','-','BKG',undefined,undefined,undefined,undefined,'MCAL background rate');
Ihf12 = new fld('T50<br>(s)','0','-','-','-','T50',undefined,undefined,undefined,undefined,'50% burst duration (s)');
Ihf13 = new fld('err_T50<br>(s)','0','-','-','-','err_T50',undefined,undefined,undefined,undefined,'50% burst duration error (s)');
Ihf14 = new fld('BKGSUB_CTS_T50','h','-','-','-','BKGSUB_CTS_T50',undefined,undefined,undefined,undefined,'MCAL background-subtracted counts in T50');
Ihf15 = new fld('T90<br>(s)','0','-','-','-','T90',undefined,undefined,undefined,undefined,'90% burst duration (s)');
Ihf16 = new fld('err_T90<br>(s)','0','-','-','-','err_T90',undefined,undefined,undefined,undefined,'90% burst duration error (s)');
Ihf17 = new fld('BKGSUB_CTS_T90','h','-','-','-','BKGSUB_CTS_T90',undefined,undefined,undefined,undefined,'MCAL background-subtracted counts in T90');
Ihf18 = new fld('LOC','0','-','-','-','LOC',undefined,undefined,undefined,undefined,'GRB localization (instrument or IPN)');
Ihf19 = new fld('THETA<br>(degrees)','h','-','-','-','THETA',undefined,undefined,undefined,undefined,'AGILE zenithal angle at T0');
Ihf20 = new fld('PHI<br>(degrees)','h','-','-','-','PHI',undefined,undefined,undefined,undefined,'AGILE azimuthal angle at T0');
Ihf21 = new fld('PL_RANGE','0','-','-','-','PL_RANGE',undefined,undefined,undefined,undefined,'Energy range for power-law spectral fitting');
Ihf22 = new fld('PL_BETA','0','-','-','-','PL_BETA',undefined,undefined,undefined,undefined,'Power-law photon index');
Ihf23 = new fld('PL_BETA_emin','h','-','-','-','PL_BETA_emin',undefined,undefined,undefined,undefined,'Minimum error on power-law photon index');
Ihf24 = new fld('PL_BETA_emax','h','-','-','-','PL_BETA_emax',undefined,undefined,undefined,undefined,'Maximum error on power-law photon index');
Ihf25 = new fld('PL_RED_CHI_SQ','0','-','-','-','PL_RED_CHI_SQ',undefined,undefined,undefined,undefined,'Reduced chi square for power-law spectral fitting');
Ihf26 = new fld('PL_DOF','h','-','-','-','PL_DOF',undefined,undefined,undefined,undefined,'Degrees of freedom for power-law spectral fitting');
Ihf27 = new fld('PL_FLUX<br>(erg&nbsp;cm<sup>-2</sup>&nbsp;s<sup>-1</sup>)','0','-','-','-','PL_FLUX',undefined,undefined,undefined,undefined,'Flux from power-law model');
Ihf28 = new fld('PL_FLUENCE<br>(erg cm<sup>-2</sup>)','0','-','-','-','PL_FLUENCE',undefined,undefined,undefined,undefined,'Fluence from power-law model over T90');
Ihf29 = new fld('BAND_RANGE','h','-','-','-','BAND_RANGE',undefined,undefined,undefined,undefined,'Energy range for Band-model spectral fitting');
Ihf30 = new fld('BAND_ALPHA','h','-','-','-','BAND_ALPHA',undefined,undefined,undefined,undefined,'Photon index alpha in Band-model spectral fitting');
Ihf31 = new fld('BAND_ALPHA_emin','h','-','-','-','BAND_ALPHA_emin',undefined,undefined,undefined,undefined,'Minimum error on alpha');
Ihf32 = new fld('BAND_ALPHA_emax','h','-','-','-','BAND_ALPHA_emax',undefined,undefined,undefined,undefined,'Maximum error on alpha');
Ihf33 = new fld('BAND_BETA','h','-','-','-','BAND_BETA',undefined,undefined,undefined,undefined,'Photon index beta in Band-model spectral fitting');
Ihf34 = new fld('BAND_BETA_emin','h','-','-','-','BAND_BETA_emin',undefined,undefined,undefined,undefined,'Minimum error on beta');
Ihf35 = new fld('BAND_BETA_emax','h','-','-','-','BAND_BETA_emax',undefined,undefined,undefined,undefined,'Maximum error on beta');
Ihf36 = new fld('Ec<br>(keV)','h','-','-','-','Ec',undefined,undefined,undefined,undefined,'Critical energy in Band-model spectral fitting');
Ihf37 = new fld('Ep<br>(keV)','h','-','-','-','Ep',undefined,undefined,undefined,undefined,'Peak energy in Band-model spectral fitting');
Ihf38 = new fld('Eb<br>(keV)','h','-','-','-','Eb',undefined,undefined,undefined,undefined,'Break energy in Band-model spectral fitting');
Ihf39 = new fld('BAND_RED_CHI_SQ','h','-','-','-','BAND_RED_CHI_SQ',undefined,undefined,undefined,undefined,'Reduced chi square for Band-model spectral fitting');
Ihf40 = new fld('BAND_DOF','h','-','-','-','BAND_DOF',undefined,undefined,undefined,undefined,'Degrees of freedom for Band-model spectral fitting');
Ihf41 = new fld('BAND_FLUX<br>(erg&nbsp;cm<sup>-2</sup>&nbsp;s<sup>-1</sup>)','h','-','-','-','BAND_FLUX',undefined,undefined,undefined,undefined,'Flux from Band model');
Ihf42 = new fld('BAND_FLUENCE<br>(erg cm<sup>-2</sup>)','h','-','-','-','BAND_FLUENCE',undefined,undefined,undefined,undefined,'Fluence from Band model');

Head = new tabRow(Ihf0,Ihf1,Ihf2,Ihf3,Ihf4,Ihf5,Ihf6,Ihf7,Ihf8,Ihf9,Ihf10,Ihf11,Ihf12,Ihf13,Ihf14,Ihf15,Ihf16,Ihf17,Ihf18,Ihf19,Ihf20,Ihf21,Ihf22,Ihf23,Ihf24,Ihf25,Ihf26,Ihf27,Ihf28,Ihf29,Ihf30,Ihf31,Ihf32,Ihf33,Ihf34,Ihf35,Ihf36,Ihf37,Ihf38,Ihf39,Ihf40,Ihf41,Ihf42); 

// load full header
function loadrow(a) {
 with(a){
  irh0  = new rowField(NAME,'-','-');
  irh1  = new rowField(ra,radeg,'-');
  irh2  = new rowField(dec,decdeg,'-');
  irh3  = new rowField(lii,'-','-'); 
  irh4  = new rowField(bii,'-','-'); 
  irh5  = new rowField(T0,MET,'-');
  irh6  = new rowField(Orbit,'-','-');
  irh7  = new rowField(RM_SA,'-','-');
  irh8  = new rowField(RM_AC,'-','-');
  irh9  = new rowField(RM_MCAL,'-','-');
  irh10 = new rowField(MCAL,'-','-');
  irh11 = new rowField(BKG,'-','-');
  irh12 = new rowField(T50,'-','-');
  irh13 = new rowField(err_T50,'-','-');
  irh14 = new rowField(BKGSUB_CTS_T50,'-','-');
  irh15 = new rowField(T90,'-','-');
  irh16 = new rowField(err_T90,'-','-');
  irh17 = new rowField(BKGSUB_CTS_T90,'-','-');
  irh18 = new rowField(LOC,'-','-');
  irh19 = new rowField(THETA,'-','-');
  irh20 = new rowField(PHI,'-','-');
  irh21 = new rowField(PL_RANGE,'-','-');
  irh22 = new rowField(PL_BETA,'-','-');
  irh23 = new rowField(PL_BETA_emin,'-','-');
  irh24 = new rowField(PL_BETA_emax,'-','-');
  irh25 = new rowField(PL_RED_CHI_SQ,'-','-');
  irh26 = new rowField(PL_DOF,'-','-');
  irh27 = new rowField(PL_FLUX,'-','-');
  irh28 = new rowField(PL_FLUENCE,'-','-');
  irh29 = new rowField(BAND_RANGE,'-','-');
  irh30 = new rowField(BAND_ALPHA,'-','-');
  irh31 = new rowField(BAND_ALPHA_emin,'-','-');
  irh32 = new rowField(BAND_ALPHA_emax,'-','-');
  irh33 = new rowField(BAND_BETA,'-','-');
  irh34 = new rowField(BAND_BETA_emin,'-','-');
  irh35 = new rowField(BAND_BETA_emax,'-','-');
  irh36 = new rowField(Ec,'-','-');
  irh37 = new rowField(Ep,'-','-');
  irh38 = new rowField(Eb,'-','-');
  irh39 = new rowField(BAND_RED_CHI_SQ,'-','-');
  irh40 = new rowField(BAND_DOF,'-','-');
  irh41 = new rowField(BAND_FLUX,'-','-');
  irh42 = new rowField(BAND_FLUENCE,'-','-');

  row = new tabRow(irh0,irh1,irh2,irh3,irh4,irh5,irh6,irh7,irh8,irh9,irh10,irh11,irh12,irh13,irh14,irh15,irh16,irh17,irh18,irh19,irh20,irh21,irh22,irh23,irh24,irh25,irh26,irh27,irh28,irh29,irh30,irh31,irh32,irh33,irh34,irh35,irh36,irh37,irh38,irh39,irh40,irh41,irh42);
 }
 return row; 
}

function writeTop() {
text  ="<div id='catalog'>\n"
text +=" <center><br>\n"

//SEZIONE TITOLO 
text +="  <font size=+3 color=navy><b>The Second AGILE-MCAL GRB Catalog</b></font><br><br>\n"
text +="  <font size=+1 color=navy>AGILE GRBs observed from November 2007 to November 2020<br/><br/>\n"
//SEZIONE BOX dei 6 bottoni + BOX Immagine aitoff + BOX VO 
text +="  <table border=0 style='font-size:14px;>\n"
text +="   <tr valign='top'>\n"
text +="    <td valign='top'>\n" //TD1 (6 bottoni)
text +=      write_image('none','none');
text +="    </td>\n";
text +="    <td width=10px valign=center>\n" //TD2 (vuoto)
text +="    </td>\n"
text +="    <td align=center valign=top  width=680px>\n" //TD3 (immagine)
text +="     <a href='mcal2grbcat_ait.png' target='_blank'>\n"
text +="      <img src=mcal2grbcat_ait.png title='Click to view' width=680px/>\n"
text +="     </a><br><br>\n"
text +="    </td>\n"
text +="    <td width=10px valign=center>\n" //TD4 (vuoto)
text +="    </td>\n"
text +="    <td id='tdsamp' valign=top align=center width=220px'>\n" //TD5 (VO panel)
text += "    <div id='samp' class='sampstyle'>"
text += "    </div>"
text +="     <div id='radecsearch' style='text-align:left;font-size:12px;border:1px solid grey;padding:10px 10px 10px 10px;'>\n"
text +=       createsearchform();
text +="     </div>\n"
text +="    </td>\n"
text +="   </tr>\n"
text +="  </table><br>\n" 

//SEZIONE Reference/Descrizione Catalogo + tab colorati ecc. 
text +="  <table border=0 style='font-size:14px;'>\n"
text +="   <tr valign='top'>\n"
text +="    <td align=center valign=top >\n"
text +="     <h1 id='author_catalog_bg'>\n"
text +="      This is the interactive version of \"The Second AGILE-MCAL GRB Catalog\", \n"
text +="      <a href='https://iopscience.iop.org/article/10.3847/1538-4357/ac3df7/pdf' target='blank'>A. Ursi et al., ApJ 925 (2022)</a>. DOI: <a href='https://iopscience.iop.org/article/10.3847/1538-4357/ac3df7' target='blank'>10.3847/1538-4357/ac3df7</a>\n"
text +="     </h1>\n"
text +="     <h1 id='comment_catalog_bg'>\n"
text +="      The catalog consists of 503 bursts, 363 of which have been localized, and are plotted in the figure above (Aitoff projection in galactic coordinates).<br>\n"
text +=" This webpage also provides access to additional AGILE data products through the \"GRB Explorer\" tool, under the \"Access to AGILE data products\" tab.\n"
text +="     </h1><br>\n"
text +="     <a href=javascript:localizedGRB('ALL');resetPagePar();nextpage();writeBottom() class='linktype1' style='color:black;background-color:white;'>ALL</a>\n"
text +="     <a href=javascript:localizedGRB('FULL');resetPagePar();nextpage();writeBottom() class='linktype1' style='color:white;background-color:grey;'>Fully acquired</a>\n" 
text +="     <a href=javascript:localizedGRB('YES');resetPagePar();nextpage();writeBottom(); class='linktype1' style='color:white;background-color:red;'>Localized</a>\n"
text +="     <a href=javascript:localizedGRB('NO');resetPagePar();nextpage();writeBottom() class='linktype1' style='color:white;background-color:navy;'>Others</a>\n"
text +="     <br><br>\n"
text +="    </td>\n"
text +="   </tr>\n"
text +="  </table>\n"
text +=   write_buttons();
text +=   display_page_raw();
text +="  <a name='start_page'></a>\n"
writeit(text,'top');
text +=" </center>\n"
text +="</div>\n"
}
