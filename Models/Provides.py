from config import db


class AdministrativeRegion(db.Model):
    __bind_key__ = 'provide'
    __tablename__ = 'administrative_regions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    name_en = db.Column(db.String(255), nullable=False)
    code_name = db.Column(db.String(255))
    code_name_en = db.Column(db.String(255))


class AdministrativeUnit(db.Model):
    __bind_key__ = 'provide'
    __tablename__ = 'administrative_units'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255))
    full_name_en = db.Column(db.String(255))
    short_name = db.Column(db.String(255))
    short_name_en = db.Column(db.String(255))
    code_name = db.Column(db.String(255))
    code_name_en = db.Column(db.String(255))


class Province(db.Model):
    __bind_key__ = 'provide'
    __tablename__ = 'provinces'

    code = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    name_en = db.Column(db.String(255))
    full_name = db.Column(db.String(255), nullable=False)
    full_name_en = db.Column(db.String(255))
    code_name = db.Column(db.String(255))
    administrative_unit_id = db.Column(db.Integer, db.ForeignKey('administrative_units.id'))
    administrative_region_id = db.Column(db.Integer, db.ForeignKey('administrative_regions.id'))


class District(db.Model):
    __bind_key__ = 'provide'
    __tablename__ = 'districts'

    code = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    name_en = db.Column(db.String(255))
    full_name = db.Column(db.String(255))
    full_name_en = db.Column(db.String(255))
    code_name = db.Column(db.String(255))
    province_code = db.Column(db.String(20), db.ForeignKey('provinces.code'))
    administrative_unit_id = db.Column(db.Integer, db.ForeignKey('administrative_units.id'))


class Ward(db.Model):
    __bind_key__ = 'provide'
    __tablename__ = 'wards'

    code = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    name_en = db.Column(db.String(255))
    full_name = db.Column(db.String(255))
    full_name_en = db.Column(db.String(255))
    code_name = db.Column(db.String(255))
    district_code = db.Column(db.String(20), db.ForeignKey('districts.code'))
    administrative_unit_id = db.Column(db.Integer, db.ForeignKey('administrative_units.id'))