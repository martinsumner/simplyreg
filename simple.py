import tornado.ioloop
import tornado.web
import plates
import os
import sys
import re

LIST_PARAM = re.compile(r"^[A-Z]+$")
SEARCH_PARAM = re.compile(r"^[A-Za-z0-9 ]+$")

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")

class WPHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("wordpress.html")

class TestHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index_test.html")

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
        try:
            searchStr = self.get_argument("search")
            if searchStr:
                if self.validate_regex(SEARCH_PARAM, searchStr):
                    results = self.dealer_plates.match_plate(searchStr.upper())
                    self.render("search.html", 
                                result_count=len(results), 
                                search_term=searchStr.upper(), 
                                results=results,
                                search_type="search")
                else:
                    self.invalid_input()
            else:
                raise tornado.web.MissingArgumentError("search")  
        except tornado.web.MissingArgumentError:
            self.render("search.html", search_term=None)

class ListHandler(RegistrationHandler):

    def get(self):
        try:
            beginsStr = self.get_argument("begins")
            if beginsStr:
                if self.validate_regex(LIST_PARAM, beginsStr):
                    results = self.dealer_plates.alphabet_list(beginsStr.upper())
                    self.render("search.html", 
                                result_count=len(results), 
                                search_term=beginsStr.upper(), 
                                results=results,
                                search_type="list by")
                else:
                    self.invalid_input()
            else:
                raise tornado.web.MissingArgumentError("begins")
        except tornado.web.MissingArgumentError:
            self.render("search.html", search_term=None)    
        


def make_app():
    dealers = [("dealer1", True), ("dealer2", False)]
    dealer_plates = plates.Plates(dealers)
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/index.html", MainHandler),
        (r"/wordpress.html", WPHandler),
        (r"/search", SearchHandler, dict(dealer_plates = dealer_plates)),
        (r"/list", ListHandler, dict(dealer_plates = dealer_plates)),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {"path" : "css/"}),
        (r"/images/(.*)", tornado.web.StaticFileHandler, {"path" : "images/"}),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(sys.argv[1])
    tornado.ioloop.IOLoop.current().start()