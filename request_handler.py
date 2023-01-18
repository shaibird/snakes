import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_snakes, get_single_snake, get_single_owner, get_all_owners, get_all_species, get_single_species, get_snakes_by_species, create_snake

class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""
        
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/') 
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    def do_GET(self):
        """Handles GET requests to the server
        """

        aonyx_cinerea = False
        success = False
        
        response = {}

        parsed = self.parse_url(self.path)

        #I think this is where we are checking if the resource is in our resources. Should have taken better notes to start
        if '?' not in self.path:
            (resource, id) = parsed

            if resource == "snakes":
                if id is not None:
                    response = f"{get_single_snake(id)}"
                    success = True
                    if not response or response =='[]':
                        aonyx_cinerea = True
                else:
                    response = f"{get_all_snakes()}"
                    success = True
            elif resource == "owners":
                if id is not None:
                    response  = f"{get_single_owner(id)}"
                    success = True
                else:
                    response = f"{get_all_owners()}"
                    success = True
            elif resource == "species":
                if id is not None:
                    response = f"{get_single_species(id)}"
                    success = True
                else:
                    response = f"{get_all_species()}"
                    success = True
        else:
            (resource, query) = parsed

            if query.get('species') and resource == 'snakes':
                response = get_snakes_by_species(query['species'][0])
                success = True
                
        if aonyx_cinerea:
            self._set_headers(405)
        else:
            if success:
                self._set_headers(200)
                self.wfile.write(json.dumps(response).encode())
            else:
                self._set_headers(404)
        
        
    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """ Handles POST requests to the server """
        
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        new_object = None
 
        if resource == "snakes":
            new_object = create_snake(post_body)

        if new_object == "missing information":
            self._set_headers(400)
        else:
            self._set_headers(201)

        self.wfile.write(json.dumps(new_object).encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        """Handles PUT requests to the server"""
        self.do_PUT()

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
