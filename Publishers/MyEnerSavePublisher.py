import pycurl, StringIO, re

class MyEnerSavePublisher :

    def __init__(self, config):
        try:
            self.token = config.get("myenersave", "token")
            self.push_url = config.get("myenersave", "push_url")
            self.h_measures = {}
            self.nb_call = 0
        except:

            try:
                self.password = config.get("myenersave", "password")
                self.login = config.get("myenersave", "login")
            except:
                if not (hasattr(self, "login") and hasattr(self, "password")):
                    print "Disabling myenersave publisher : pleaser add your login/password in config file"
                    raise NameError("Missing config key(s) => disabling") 

            # create token
            
            c = pycurl.Curl()
            # login
            print "Logging-in as %s:****" % self.login
            c.setopt(c.POST, 1)
            c.setopt(c.URL, "https://myenersave.com/user?destination=front_page")
            c.setopt(c.HTTPPOST, [("name", self.login),
                                    ("pass", self.password),
                                    ("form_id", "user_login"),
                                    ("op", "Log in") ])
            c.setopt(c.COOKIEFILE, "")
            c.perform()

            print "Creating token"            
            c.setopt(c.HTTPGET, 1)
            c.setopt(c.URL, "https://data.myenersave.com/fetcher/bind?mfg=currentcost&model=envir")
            c.setopt(c.FOLLOWLOCATION, 1)
            s = StringIO.StringIO()
            c.setopt(pycurl.WRITEFUNCTION, s.write)
            c.perform()
            resp = s.getvalue()

            c.close()

            # pqrse HTML and retrieve infos
            m = re.search("<b>Host URL: </b>(.*?)<br>", resp)
            self.push_url = m.group(1)

            m = re.search("<b>Activation Token: </b>(.*?)<br>", resp)
            self.token = m.group(1)

            print "storing response push_url:%s, token:%s" % (self.push_url, self.token)
            config.set("myenersave", "token", self.token)
            config.set("myenersave", "push_url", self.push_url)
            config.remove_option("myenersave", "login")
            config.remove_option("myenersave", "password")
            pass


    def refreshRate(self):
        return 6


    # max posting rate 1 POST/60sec
    def publish(self, since, to, watt, temp):
        try:
            self.nb_call += 1

            # store data
            self.h_measures[to] = watt

            if(self.nb_call > 60/self.refreshRate()):
                xml_data = ""
                for ts, power in iter(sorted(self.h_measures.iteritems())):
                    xml_data += "<energy time=\"%s\" wh=\"%s\"/>" % (ts, power)

                xml = "<upload><sensor type=\"0\">%s</sensor></upload>" % xml_data

                c = pycurl.Curl()
                c.setopt(c.POST, 1)
                c.setopt(c.URL, self.push_url)
                c.setopt(c.HTTPHEADER,["Content-Type: application/xml", "token: %s" % self.token])
                c.setopt(c.POSTFIELDS, xml)
                #c.setopt(c.VERBOSE, 1)
                c.perform()
                ok = c.getinfo(c.HTTP_CODE)
                c.close()
                # 200 ?
                if ok == 200:
                    self.nb_call = 0
                    self.h_measures.clear()

        except Exception as e:
            print e
            print "Error occured while publishing on myenersave.com :("
            return False
        
        print "Temperature (not supported) : %i" % temp
        return True
