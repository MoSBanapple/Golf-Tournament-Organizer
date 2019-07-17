import unittest
import requests

baseurl = "https://golforganizer.appspot.com"

class TestTournament(unittest.TestCase):
    
    def test_Tournament(self):
        testparams = {
        "name":"testName",
        "host":"alex",
        "date":"1/2/2003",
        "time":"10:00 AM",
        "fee":12.53,
        "courseid":123,
        "scores":["bob 1", "jack 2 3"]
        }
        r1 = requests.post(url = baseurl + "/tournaments", data = testparams)
        data = r1.json()
        id = data["id"]
        self.assertEqual(data["name"], "testName")
        self.assertEqual(data["host"], "alex")
        self.assertEqual(data["date"], "1/2/2003")
        self.assertEqual(data["time"], "10:00 AM")
        self.assertEqual(data["fee"], 12.53)
        self.assertEqual(data["courseid"], 123)
        self.assertEqual(data["scores"][0], "bob 1")
        self.assertEqual(data["scores"][1], "jack 2 3")
        data2 = requests.get(url = baseurl + "/tournaments/" + str(id)).json()
        for k in data.keys():
            self.assertEqual(data[k], data2[k])
        data3 = requests.get(url = baseurl + "/tournaments").json()
        counter = 0
        for tournament in data3["tournaments"]:
            if tournament["id"] == id:
                counter += 1
                for k in data.keys():
                    self.assertEqual(tournament[k], data[k])
        self.assertEqual(counter, 1)
        testparams["name"] = "modName"
        testparams["time"] = "11:00 AM"
        testparams["scores"] = ["bob 1 2", "jack 2 3 2", "andrew 9"]
        dataPut = requests.put(url = baseurl + "/tournaments/" + str(id), data = testparams).json()
        self.assertEqual(dataPut["name"], "modName")
        self.assertEqual(dataPut["time"], "11:00 AM")
        self.assertEqual(dataPut["scores"], ["bob 1 2", "jack 2 3 2", "andrew 9"])
        rDelete = requests.delete(url = baseurl + "/tournaments/" + str(id))
        rFaultget = requests.get(url = baseurl + "/tournaments/" + str(id)).text
        self.assertEqual(rFaultget, "null")


    def test_User(self):
        testparams = {
        "username":"testName",
        "playing":[123, 456],
        "hosting":[789],
        }
        r1 = requests.post(url = baseurl + "/users", data = testparams)
        data = r1.json()
        self.assertEqual(data["username"], "testName")
        self.assertEqual(data["playing"], [123, 456])
        self.assertEqual(data["hosting"], [789])
        data2 = requests.get(url = baseurl + "/users/testName").json()
        for k in data.keys():
            self.assertEqual(data[k], data2[k])
        data3 = requests.get(url = baseurl + "/users").json()
        counter = 0
        for user in data3["users"]:
            if user["username"] == "testName":
                counter += 1
                for k in data.keys():
                    self.assertEqual(user[k], data[k])
        self.assertEqual(counter, 1)
        testparams["playing"] = [12, 34, 56]
        dataPut = requests.put(url = baseurl + "/users/testName", data = testparams).json()
        self.assertEqual(dataPut["playing"], [12, 34, 56])
        rDelete = requests.delete(url = baseurl + "/users/testName")
        rFaultget = requests.get(url = baseurl + "/users/testName").text
        self.assertEqual(rFaultget, "null")

    def test_Course(self):
        testparams = {
        "name":"testName",
        "id":99999,
        "location":"123 example way",
        "par": [3,4,3,5,4,5,4,3,4,5,4,3,4,3,3,4,5,5]
        }
        r1 = requests.post(url = baseurl + "/courses", data = testparams)
        data = r1.json()
        self.assertEqual(data["name"], "testName")
        self.assertEqual(data["id"], 99999)
        self.assertEqual(data["location"], "123 example way")
        self.assertEqual(data["par"], [3,4,3,5,4,5,4,3,4,5,4,3,4,3,3,4,5,5])
        data2 = requests.get(url = baseurl + "/courses/99999").json()
        for k in data.keys():
            self.assertEqual(data[k], data2[k])
        data3 = requests.get(url = baseurl + "/courses").json()
        counter = 0
        for course in data3["courses"]:
            if course["id"] == 99999:
                counter += 1
                for k in data.keys():
                    self.assertEqual(course[k], data[k])
        self.assertEqual(counter, 1)
        testparams["par"] = [12, 34, 56]
        dataPut = requests.put(url = baseurl + "/courses/99999", data = testparams).json()
        self.assertEqual(dataPut["par"], [12, 34, 56])
        rDelete = requests.delete(url = baseurl + "/courses/99999")
        rFaultget = requests.get(url = baseurl + "/courses/99999").text
        self.assertEqual(rFaultget, "null")

if __name__ == '__main__':
    unittest.main()