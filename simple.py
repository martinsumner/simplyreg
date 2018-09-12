import tornado.ioloop
import tornado.web
import plates
import os
import sys
import re

LIST_PARAM = re.compile(r"^[A-Z]+$")
SEARCH_PARAM = re.compile(r"^[A-Za-z0-9]+$")

class MainHandler(tornado.web.RequestHandler):

    def get_template_path(self):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, "templates")

    def get(self):
        self.render("index.html")

class RegistrationHandler(MainHandler):

    def initialize(self, dealer_plates):
        self.dealer_plates = dealer_plates
    
    def validate_regex(self, regex, param):
        if regex.match(param):
            return True
        else:
            return False

    def invalid_input(self):
        self.render("invalid_input.html")

class SearchHandler(RegistrationHandler):

    def get(self):
        searchStr = self.get_argument("search")
        if self.validate_regex(SEARCH_PARAM, searchStr):
            results = self.dealer_plates.match_plate(searchStr.upper())
            self.render("search_results.html", 
                        result_count=len(results), 
                        search_term=searchStr.upper(), 
                        results=results)
        else:
            self.invalid_input()

class ListHandler(RegistrationHandler):

    def get(self):
        beginsStr = self.get_argument("begins")
        if self.validate_regex(LIST_PARAM, beginsStr):
            results = self.dealer_plates.alphabet_list(beginsStr.upper())
            self.render("list_results.html", 
                        result_count=len(results), 
                        alphabet_term=beginsStr.upper(), 
                        results=results)
        else:
            self.invalid_input()
        


def make_app():
    dealers = [("dealer1", True), ("dealer2", False)]
    dealer_plates = plates.Plates(dealers)
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/search", SearchHandler, dict(dealer_plates = dealer_plates)),
        (r"/list", ListHandler, dict(dealer_plates = dealer_plates)),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(sys.argv[1])
    tornado.ioloop.IOLoop.current().start()