import pycurl, StringIO, re

class MyEnerSavePublisher :

    def __init__(self, config):
        try:
            self.token = config.get("myenersave", "token")
            self.push_url = config.get("myenersave", "push_url")
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

    def publish(self, since, to, watt, temp):
        print "myenersave (token %s)" % self.token
        return True
        try:
            kwatt = watt / 1000
            c = pycurl.Curl()
            c.setopt(c.POST, 1)
            c.setopt(c.URL, "http://%s:@plotwatt.com/api/v2/push_readings" % self.house_secret)
            c.setopt(c.POSTFIELDS, "%s,%s,%s" % (self.meter_id, kwatt, since))
            #c.setopt(c.VERBOSE, 1)
            c.perform()
            c.close()
        except Exception as e:
            print e
            print "Error occured while publishing on plotwatt.com :("
            return False
        
        #print "POST curl -d %i,%f,%i http://%s@plotwatt.com/api/v2/push_readings" % (self.meter_id, watt, since, self.house_secret)
        print "Temperature (not supported) : %i" % temp
        return True
