import pycurl, StringIO, json

class PlotwattPublisher :

    def __init__(self, config):
        try:
            self.house_secret = config.get("plotwatt", "house_secret")
            self.meter_id = config.get("plotwatt", "meter_id")
        except:

            if not hasattr(self, "house_secret"):
                print "Disabling plotwatt publisher : pleaser add your house_secret in config file"
                raise NameError("Missing config key => disabling") 

            # create meter id
            
            print "Creating meter"            
            c = pycurl.Curl()
            c.setopt(c.POST, 1)
            c.setopt(c.URL, "http://%s:@plotwatt.com/api/v2/new_meters" % self.house_secret)
            c.setopt(c.HTTPPOST, [("numbers_of_new_meters", "1")])
            c.perform()
            print "Retrieving meter_id"
            #c.setopt(c.POST, 0)
            c.setopt(c.URL, "http://%s:@plotwatt.com/api/v2/list_meters" % self.house_secret) 
            s = StringIO.StringIO()
            c.setopt(pycurl.WRITEFUNCTION, s.write)
            c.perform()
            meters = json.loads(s.getvalue())

            c.close()

            self.meter_id = meters[0]

            config.set("plotwatt", "meter_id", self.meter_id)
            pass


    def refreshRate(self):
        return 6

    def publish(self, since, to, watt, temp):
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
