class HeadingPlan:
    def __init__(self, nav,
            waypoint=ll.LatLon(50.742810, 1.014469), # somewhere in the solent
            target_radius=2,
            ):
        """Heading planning machinery, dumb version.
        
        For testing purposes, this believes that the boat can go in any
        direction, including directly upwind. It never tries to tack.
        """
        self.nav = nav
        self.waypoint = waypoint
        x, y = self.nav.latlon_to_utm(waypoint.lat.decimal_degree, waypoint.lon.decimal_degree)
        self.waypoint_xy = Point(x, y)
        self.target_area = self.waypoint_xy.buffer(target_radius)
    
    def start(self):
        pass

    def check_end_condition(self):
        return self.nav.position_xy.within(self.target_area)

    def distance_heading_to_waypoint(self):
        dx = self.waypoint_xy.x - self.nav.position_xy.x
        dy = self.waypoint_xy.y - self.nav.position_xy.y
        d = (dx**2 + dy**2) ** 0.5
        h = math.degrees(math.atan2(dx, dy)) % 360
        return d, h

    def calculate_state_and_goal(self):
        """Work out what we want the boat to do
        """
        wp_heading = self.nav.position_ll.heading_initial(self.waypoint)
        return 'normal', wp_heading
