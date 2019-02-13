
class Send:
    def __init__(self, driver, db, date_now, time_now):
        self.driver = driver
        self.db = db
        self.date_now = date_now
        self.time_now = time_now

    def single(self, target, msg, Messages, sender):
        element = self.driver.find_element_by_class_name('_35EW6')
        element.click()

        messages = Messages(sender,target, msg, self.date_now, self.time_now)
        self.db.session.add(messages)
        self.db.session.commit()

    def all(self, msg, all_contacts, time, waitForButtonSend, Messages, sender):
        driver = self.driver
        db = self.db
        for contacts in all_contacts:

            self.driver.get('https://web.whatsapp.com/send?phone=' + contacts.phone + '&text=' + msg)
            time.sleep(10)

            waitForButtonSend(driver)

            time.sleep(1)
            element = driver.find_element_by_class_name('_35EW6')
            element.click()

            messages = Messages(sender, contacts.phone, msg, self.date_now, self.time_now)
            db.session.add(messages)
            db.session.commit()

            time.sleep(5)


    def groups(self, time, joined_group, msg, Keys):
        groups_name = []
        for join_group in joined_group:
            groups_name.append(join_group.group_name)

        for group_name in groups_name:
            searchbox = self.driver.find_element_by_class_name("jN-F5")

            time.sleep(1)

            searchbox.send_keys(group_name)
            searchbox.send_keys(Keys.ENTER)

            text = self.driver.find_element_by_class_name('_2S1VP')
            text.send_keys(msg)

            time.sleep(1)
            element = self.driver.find_element_by_class_name('_35EW6')
            element.click()

            time.sleep(1)

    def cgroups(self, Messages, msg, time, selected_groups, Contacts_grouping, waitForButtonSend, sender):
        for selected in selected_groups:

            contacts = Contacts_grouping.query.filter_by(group_name=selected)
            for number in contacts:
                self.driver.get('https://web.whatsapp.com/send?phone={}&text={}'.format(number.phone, msg))

                # WAIT FOR ELEMENT SEND BUTTON CAN BE CLICKED
                waitForButtonSend(self.driver)
                time.sleep(1)

                element = self.driver.find_element_by_class_name('_35EW6')
                element.click()

                messages = Messages(sender, number.phone, msg, self.date_now, self.time_now)
                self.db.session.add(messages)
                self.db.session.commit()

                time.sleep(5)
        self.driver.close()