
class Send:
    def __init__(self, driver, db, date_now, time_now):
        self.driver = driver
        self.db = db
        self.date_now = date_now
        self.time_now = time_now

    def single(self, target, msg, Messages):
        element = self.driver.find_element_by_class_name('_35EW6')
        element.click()

        messages = Messages('081380353611',target, msg, self.date_now, self.time_now)
        self.db.session.add(messages)
        self.db.session.commit()

        self.driver.close()