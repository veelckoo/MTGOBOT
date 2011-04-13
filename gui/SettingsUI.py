from sikuli.Sikuli import *
import javax.swing
import java.awt

class SettingsUI(object):
    
    def __init__(self):
        
        self.frame = javax.swing.JFrame("MTGO BOT Settings")
        self.frame.setSize(500, 600)
        self.frame.setLayout(javax.swing.BorderLayout())
        self.build_interface()
    
        self.build_interface()
    
    def build_interface(self):
        self.general_settings()
        self.records_settings()
        self.connection_settings()
        self.trade_settings()
        self.inventory_settings()
        
    
    def general_settings(self):
        from GeneralSettings import *
        
    def records_settings(self):
        from RecordsSettings import *
        
    def connection_settings(self):
        from ConnectionSettings import *
    
    def trade_settings(self):
        from TradeSettings import *
    
    def inventory_settings(self):
        from InventorySettings import *
    
    def network_settings(self):
        #to be built after bot networking functionality has first been created and finalized
        from NetworkSettings import *
        
