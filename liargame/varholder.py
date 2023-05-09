

# Create your varholder here


class VarHolder:
    def __init__(self):
        self.vars = {}
        
    def set(self, **kwargs):
        for key, value in kwargs.items():
            # if key in self.vars:
                # warnings.warn("overwritting exitsing variable!")
            
            self.vars[key] = value
            
    def get(self, key, default=None):
        return self.vars.get(key, default)
    
    def pop(self, key, default=None):
        self.vars.pop(key, default)
        
    def remove(self, key, error_proof=False):
        if error_proof:
            self.pop(key)
        else:
            del self.vars[key]