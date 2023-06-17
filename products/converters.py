class FloatDecimalConverter:
    regex = r'\d+\.\d{2}|\d+'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)
