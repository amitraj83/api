import json

class Car:
    def __init__(self, model_id,model_make_id,model_name,model_trim,model_year,model_body,model_engine_position,model_engine_cc,model_engine_cyl,model_engine_type,model_engine_valves_per_cyl,model_engine_power_ps,model_engine_power_rpm,model_engine_torque_nm,model_engine_torque_rpm,model_engine_bore_mm,model_engine_stroke_mm,model_engine_compression,model_engine_fuel,model_top_speed_kph,model_0_to_100_kph,model_drive,model_transmission_type,model_seats,model_doors,model_weight_kg,model_length_mm,model_width_mm,model_height_mm,model_wheelbase_mm,model_lkm_hwy,model_lkm_mixed,model_lkm_city,model_fuel_cap_l,model_sold_in_us,model_co2,model_make_display, image):
        self.model_id = model_id
        self.model_make_id = model_make_id
        self.model_name = model_name
        self.model_trim = model_trim
        self.model_year = model_year
        self.model_body = model_body
        self.model_engine_position = model_engine_position
        self.model_engine_cc = model_engine_cc
        self.model_engine_cyl = model_engine_cyl
        self.model_engine_type = model_engine_type
        self.model_engine_valves_per_cyl = model_engine_valves_per_cyl
        self.model_engine_power_ps = model_engine_power_ps
        self.model_engine_power_rpm = model_engine_power_rpm
        self.model_engine_torque_nm = model_engine_torque_nm
        self.model_engine_torque_rpm = model_engine_torque_rpm
        self.model_engine_bore_mm = model_engine_bore_mm
        self.model_engine_stroke_mm = model_engine_stroke_mm
        self.model_engine_compression = model_engine_compression
        self.model_engine_fuel = model_engine_fuel
        self.model_top_speed_kph = model_top_speed_kph
        self.model_0_to_100_kph = model_0_to_100_kph
        self.model_drive = model_drive
        self.model_transmission_type = model_transmission_type
        self.model_seats = model_seats
        self.model_doors = model_doors
        self.model_weight_kg = model_weight_kg
        self.model_length_mm = model_length_mm
        self.model_width_mm = model_width_mm
        self.model_height_mm = model_height_mm
        self.model_wheelbase_mm = model_wheelbase_mm
        self.model_lkm_hwy = model_lkm_hwy
        self.model_lkm_mixed = model_lkm_mixed
        self.model_lkm_city = model_lkm_city
        self.model_fuel_cap_l = model_fuel_cap_l
        self.model_sold_in_us = model_sold_in_us
        self.model_co2 = model_co2
        self.model_make_display = model_make_display
        self.image = image

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)


class LightCar:
    def __init__(self, name, id):
        self.name = name
        self.id = id
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class Criteria:
    def __init__(self, col_name, display_name, description):
        self.col_name = col_name
        self.display_name = display_name
        self.description = description
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class Make:
    def __init__(self, value, label):
        self.value = value
        self.label = label
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class Model:
    def __init__(self, value, label):
        self.value = value
        self.label = label
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class Variant:
    def __init__(self, value, label):
        self.value = value
        self.label = label
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)


class LinkInformation:
    def __init__(self, id, car_ids, criteria, response, display_text, summary, page_title, other_data, url, carDetails, keywords):
        self.id = id
        self.car_ids = car_ids
        self.criteria = criteria
        self.response = response
        self.display_text = display_text
        self.summary = summary
        self.page_title = page_title
        self.other_data = other_data
        self.url = url
        self.carDetails = carDetails
        self.keywords = keywords
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

