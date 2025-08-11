class GlobalVars:
    _instance = None  # Singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalVars, cls).__new__(cls)
            cls._instance._vars = {}
        return cls._instance

    def add(self, key, value):
        self._vars[key] = value

    def set(self, key, value):
        if key in self._vars:
            self._vars[key] = value
        else:
            raise KeyError(f"{key} is not a global variable")

    def get(self, key, default=None):
        return self._vars.get(key, default)

    def delete(self, key):
        if key in self._vars:
            del self._vars[key]

    @property
    def all(self):
        return dict(self._vars)  # copy to avoid modification
