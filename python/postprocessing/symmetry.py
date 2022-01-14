import ROOT,math


def symmetry(hists, fUp,fDown,fNom=None,version="shape"):
    if fNom is None:
        return
    filenom = ROOT.TFile()
    filenom = ROOT.TFile.Open(fNom,"UPDATE")
    hnom = ROOT.TH1F()
    fileup = ROOT.TFile.Open(fUp,"UPDATE")
    hup = ROOT.TH1F()
    filedown = ROOT.TFile.Open(fDown,"UPDATE")
    hdown = ROOT.TH1F()
    for h in hists:
        filedown.cd()
        hdown = (ROOT.TH1F)(filedown.Get(h))
        filenom.cd()
        hnom = (ROOT.TH1F)(filenom.Get(h))
        fileup.cd()
        hup = (ROOT.TH1F)(fileup.Get(h))
        if(version=="integral"):
            hup.Scale((hnom.Integral()+(hup.Integral()-hdown.Integral())/2)/hup.Integral())
            hdown.Scale((hnom.Integral()-(hup.Integral()-hdown.Integral())/2)/hdown.Integral())
            #            print hdown.GetName(), " ", hdown.Integral()
            #            print hup.GetName(), " ", hup.Integral()
        if(version=="cureZeros"):
            for b in range(1,hnom.GetNbinsX()+1):
                bnom = hnom.GetBinContent(b)
                bnomnew= max(0.00001,bnom)
                hnom.SetBinContent(b,bnomnew)
                print "h name ", hnom.GetName()," bin ", b, " nom ",bnom, "bnew ", bnomnew
                
        if(version=="shape"):
            for b in range(1,hup.GetNbinsX()+1):
                bnom = hnom.GetBinContent(b)
                bup= hup.GetBinContent(b)
                bdown=hdown.GetBinContent(b)
                
                bupnew=bnom+abs(abs(bup-bnom)+ abs(bdown-bnom))/2.0  
                bdownnew=bnom-abs(abs(bup-bnom)+ abs(bdown-bnom))/2.0  
                
                print "h name ", hnom.GetName()," bin ", b, " nom ",bnom, " up ", bup, " hdown ", bdown, " hupnew ", bupnew, " hdownnew ", bdownnew

                hup.SetBinContent(b,bupnew)
                hdown.SetBinContent(b,bdownnew)

        if(version == "cureZeros"):
            filenom.cd()
            hnom.Write(h)

        if(version=="shape" or version == "integral" ):
            fileup.cd()
            hup.Write(h)
            print("writing ",h," into file ",fileup )
            filedown.cd()
            hdown.Write(h)
            print("writing ",h," into file ",filedown )
    filenom.Close()
    fileup.Close()
    filedown.Close()



def nnpdfeval(histos,fNom,fRMS,fUp,fDown):
    if fNom is None:
        return
    filenom = ROOT.TFile()
    filenom = ROOT.TFile.Open(fNom,"OPEN")
    hnom = ROOT.TH1F()
    fileup = ROOT.TFile.Open(fUp,"UPDATE")
    hup = ROOT.TH1F()
    filedown = ROOT.TFile.Open(fDown,"UPDATE")
    hdown = ROOT.TH1F()
    filerms = ROOT.TFile.Open(fRMS,"UPDATE")
    hrms = ROOT.TH1F()
    print("files ",fNom,fUp,fDown)
    print("histos ",histos)
    for h in histos:
        scalef=1.
        filedown.cd()
        hdown = (ROOT.TH1F)(filedown.Get(h))
        filenom.cd()
        hnom = (ROOT.TH1F)(filenom.Get(h))
        fileup.cd()
        hup = (ROOT.TH1F)(fileup.Get(h))
        filerms.cd()
        hrms = (ROOT.TH1F)(filerms.Get(h))
        scalef=hnom.Integral()/hnom.GetEntries()
        for b in range(1,hup.GetNbinsX()+1):
            bnom = hnom.GetBinContent(b)
            brms= hrms.GetBinContent(b)/scalef
            brms=math.sqrt(brms)*scalef
            bup=bnom+brms
            bdown=bnom-brms
            print( "h name ", hnom.GetName()," bin ", b, " nom ",bnom, "brms",brms, " up ", bup, " hdown ", bdown)
            hup.SetBinContent(b,bup)
            hdown.SetBinContent(b,bdown)

        fileup.cd()
        hup.Write(h)
        filedown.cd()
        hdown.Write(h)

    filenom.Close()
    fileup.Close()
    filedown.Close()
