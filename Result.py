class Result:
    def __init__(self, res, dop, src_case, fname, dt, err=None):
        self.res = res
        self.dop = dop
        self.case = src_case
        self.fname = fname
        self.dt = dt
        self.err = err

        # Exists to allow overwriting of results without needing to re-run all tests
        self.uid = f"{self.fname}-{self.dop}-{self.case.uid}"

    def __str__(self):
        if self.err:
            return f"ERR: {self.fname}@{self.dop} ({self.case}) - {self.err}"
        else:
            return f"{self.fname}@{self.dop}: {self.res} ({self.case})({self.dt}s)"
