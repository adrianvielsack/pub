# -*- coding: utf-8 -*-
"""
@author Adrian Vielsack <advielsack@gmail.com>
@license GPLv3 <http://www.gnu.org/licenses/gpl-3.0.txt>
Quick hack to display current and next talks

"""


from urllib import request as urlrequest
import simplexml, os
import datetime, time
import dateutil.parser

class Py3status:
    def _load_xml(self):
        if hasattr(self, "xml_cache"):
            return
        self.display_index = 0
        if not os.path.exists("/tmp/33c3_schedule_cache.xml"):
            request = urlrequest.urlopen("https://fahrplan.events.ccc.de/congress/2016/Fahrplan/schedule.xml")
            data = request.read()
            with open("/tmp/33c3_schedule_cache.xml", "wb") as fp:
                fp.write(data)
        else:
            with open("/tmp/33c3_schedule_cache.xml", "rb") as fp:
                data = fp.read()
        data = data.decode("utf-8")
        xml = simplexml.loads(data)
        xml_cache = []
        for day in range(0, 4):
            for room in range(0, 4):
                tmp = xml["schedule"]["day"][day]["room"][room]["event"]
                for n in tmp:
                   date, title, place = dateutil.parser.parse(n["date"]).replace(tzinfo=None), n["title"], n["room"]
                   xml_cache.append({"date": date, "title": title, "place": place, "start": n["start"]})
        self.xml_cache = sorted(xml_cache, key=lambda x: x["date"].timestamp())
    def ccc(self, i3s_output_list, i3s_config):
        self._load_xml()
        now = datetime.datetime.now()
        self.xml_cache = [n for n in self.xml_cache if ((n["date"] - now).seconds + (n["date"] - now).days * (3600 * 24)) + (15 * 60) > 0]
        to_display= [n for n in self.xml_cache if int(n["date"].timestamp() - now.timestamp()) in range(-20 * 60, 3600)]
        if len(to_display) > 0:
            self.display_index = (self.display_index + 1) % len(to_display)
            td = to_display[self.display_index]
            print(td["date"], now, td["date"] - now)
            text = "%s: %s (%s)" % (td["start"], td["title"], td["place"])
        else:
            text = ""
        return {
            'full_text': self.py3.safe_format("33C3: %s" % text,1),
             'cached_until': time.time() + 5
        }


if __name__ == "__main__":
    from py3status.module_test import module_test
    module_test(Py3status)
