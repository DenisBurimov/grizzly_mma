from app import db


class ModelMixin(object):
    def save(self, auto_commit=True):
        # Save this model to the database.
        db.session.add(self)
        if auto_commit:
            db.session.commit()
        return self


# Add your own utility classes and functions here.
