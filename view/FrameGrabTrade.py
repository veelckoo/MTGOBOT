from sikuli.Sikuli import *
path_to_bot = getBundlePath().rsplit("\\", 1)[0] + "\\"

class FrameGrabTrade(object):
    """
    Used to get specific areas of the interface during a trade transaction
    """
    
    def get_trade_frame(self, app_region, phase, frame_name, subsection):
    
        scales = {"height": 768 / app_region.getH(), "width": 1024 / app_region.getW()}
        print("app region: " + str(app_region.x) + " " + str(app_region.y) + " " + str(app_region.w) + " " + str(app_region.h))
        print("scales are :" + str(scales["width"]) + " " + str(scales["height"]))
        if phase == "preconfirm":
        
            if frame_name == "collection":
                return self.collection_window(app_region=app_region, scales=scales, subsection=subsection)
            elif frame_name == "giving_window":
                return self.giving_window(app_region=app_region, scales=scales, subsection=subsection)
            elif frame_name == "taking_window":
                return self.taking_window(app_region=app_region, scales=scales)
                
        elif phase == "confirm":
           
            if frame_name == "giving_window":
                return self.confirm_giving_window(app_region=app_region, scales=scales, subsection=subsection)
            elif frame_name == "taking_window":
                return self.confirm_taking_window(app_region=app_region, scales=scales, subsection=subsection)
                
    def collection_window(self, app_region, scales, subsection):
        """
        Valid strings for subsection: 
        product_name_area,
        product_quantity_area,
        *product_rarity_area,
        *product_set_area
        """
        
        sections = {"product_name_area": Region((app_region.getX() + 16) * scales["width"],
                                               (app_region.getY() + 116) * scales["height"],
                                               159 * scales["width"],
                                               18 * scales["height"]),
                    "product_quantity_area": Region((app_region.getX() + 176) * scales["width"],
                                                   (app_region.getY() + 116) * scales["height"],
                                                   40 * scales["width"],
                                                   18 * scales["height"]),
                    "product_set_area": Region((app_region.getX() + 298) * scales["width"],
                                                (app_region.getY() + 116) * scales["height"],
                                                63 * scales["width"],
                                                18 * scales["height"]),
                    "product_rarity_area": Region((app_region.getX() + 218) * scales["width"],
                                                  (app_region.getY() + 116) * scales["height"],
                                                  79 * scales["width"],
                                                  18 * scales["height"])}
        return sections[subsection]
    
    def searchfield(self, app_region):
        scales = {"height": 768 / app_region.getH(), "width": 1024 / app_region.getW()}
        return Location((app_region.getX() + 70) * scales["width"], (app_region.getY() + 45) * scales["height"])
        
    def searchbutton(self, app_region):
        scales = {"height": 768 / app_region.getH(), "width": 1024 / app_region.getW()}
        return Location((app_region.getX() + 30) * scales["width"], (app_region.getY() + 45) * scales["height"])
    
    def giving_window(self, app_region, scales, subsection):
        """
        Valid strings for subsection: 
        product_name_area,
        product_quantity_area
        """
        
        section = {"product_name_area": Region((app_region.x + 19) * scales["width"],
                                               (app_region.y + 619) * scales["height"],
                                               198 * scales["width"],
                                               17 * scales["height"]),
                   "product_quantity_area": Region((app_region.x + 18) * scales["width"],
                                                   (app_region.y + 619) * scales["height"],
                                                   32 * scales["width"],
                                                   17 * scales["height"])}
        return section[subsection]
    
    def taking_window(self, app_region, scales, subsection):
        """
        Valid strings for subsection: 
        product_name_area,
        product_quantity_area
        """
        
        section = {"product_name_area": Region((app_region.x+443) * scales["width"],
                                               (app_region.y+619) * scales["height"],
                                               198 * scales["width"],
                                               17 * scales["height"]),
                   "product_quantity_area": Region((app_region.x + 411) * scales["width"],
                                                   (app_region.y + 619) * scales["height"],
                                                   32 * scales["width"],
                                                   17 * scales["height"])}
    
        return section[subsection]
        
    def confirm_taking_window(self, app_region, scales, subsection):
        
        section = {"product_quantity_area":Region((app_region.getX() + 18) * scales["width"],
                                                  (app_region.getY() + 89) * scales["height"],
                                                  34 * scales["width"],
                                                  17 * scales["height"]),
                   "product_name_area": Region((app_region.getX() + 52) * scales["width"],
                                               (app_region.getY() + 90) * scales["height"],
                                               163 * scales["width"],
                                               17 * scales["height"]),
                   "product_rarity_area": Region((app_region.x + 647) * scales["width"],
                                                 (app_region.y + 90) * scales["height"],
                                                 61 * scales["width"],
                                                 17 * scales["height"]),
                   "product_set_area": Region((app_region.x + 599) * scales["width"],
                                              (app_region.y + 90) * scales["height"],
                                              45 * scales["width"],
                                              17 * scales["height"])}
        return section[subsection]
        
    def confirm_giving_window(self, app_region, scales, subsection):
    
        section = {"product_quantity_area":Region((app_region.getX() + 16) * scales["width"],
                                                  (app_region.getY() + 439) * scales["height"],
                                                  36 * scales["width"],
                                                  17 * scales["height"]),
                   "product_name_area": Region((app_region.getX() + 50) * scales["width"],
                                               (app_region.getY() + 440) * scales["height"],
                                               163 * scales["width"],
                                               17 * scales["height"]),
                   "product_rarity_area": Region((app_region.getX() + 645) * scales["width"],
                                                 (app_region.getY() + 440) * scales["height"],
                                                 63 * scales["width"],
                                                 17 * scales["height"]),
                   "product_set_area": Region((app_region.getX() + 597) * scales["width"],
                                              (app_region.getY() + 440) * scales["height"],
                                              47 * scales["width"],
                                              17 * scales["height"])}
        return section[subsection]