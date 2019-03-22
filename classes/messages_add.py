
class Send:
    def __init__(self, driver, db, date_now, time_now, time, Keys):
        self.driver = driver
        self.db = db
        self.date_now = date_now
        self.time_now = time_now
        self.time = time
        self.Keys = Keys

    def single(self, target, msg, Messages, sender, waitForButtonSend,isFile,imagePath):
        waitForButtonSend(self.driver)

        if (isFile):
            success = False

            while (success == False):
                try:
                    iconBtn = self.driver.find_element_by_css_selector("span[data-icon='clip']")
                    iconBtn.click()

                    uploadFile = self.driver.find_element_by_css_selector('input[type=file]')
                    uploadFile.send_keys(imagePath)

                    self.time.sleep(2)

                    self.driver.find_element_by_css_selector(".bsmJe > div:nth-child(2)").send_keys(msg)
                    element = self.driver.find_element_by_css_selector("span[data-icon='send-light']")
                    element.click()

                    success = True
                except:
                    success = False
        else:
            element = self.driver.find_element_by_class_name('_35EW6')
            element.click()
        messages = Messages(sender,target, msg, self.date_now, self.time_now)
        self.db.session.add(messages)
        self.db.session.commit()

    def all(self, msg, all_contacts, time, waitForButtonSend, Messages, sender, isFile,imagePath,app):
        driver = self.driver
        db = self.db
        for contacts in all_contacts:

            self.driver.get('https://web.whatsapp.com/send?phone=' + contacts.phone + '&text=' + msg)
            time.sleep(10)

            waitForButtonSend(driver)

            if (isFile):
                # success = False
                #
                # while (success == False):
                #     try:
                self.time.sleep(1)
                iconBtn = self.driver.find_element_by_css_selector("span[data-icon='clip']")
                iconBtn.click()

                self.time.sleep(2)

                uploadFile = self.driver.find_element_by_css_selector('input[type=file]')
                uploadFile.send_keys(imagePath)

                self.time.sleep(2)

                textbox = self.driver.find_element_by_css_selector(".bsmJe > div:nth-child(2)")
                textbox.send_keys(msg)
                textbox.send_keys(self.Keys.ENTER)

                # element = self.driver.find_element_by_css_selector("span[data-icon='send-light']")
                # element.click()

                break
                    # except BaseException as e:
                    #     app.logger.info(e)
                    #     success = False
            else:

                time.sleep(1)
                element = driver.find_element_by_class_name('_35EW6')
                element.click()

            messages = Messages(sender, contacts.phone, msg, self.date_now, self.time_now)
            db.session.add(messages)
            db.session.commit()

            time.sleep(5)


    def groups(self,sender, Messages, time, joined_group, msg, Keys, isFile,imagePath):
        groups_name = []
        for join_group in joined_group:
            groups_name.append(join_group.group_name)

        for group_name in groups_name:
            searchbox = self.driver.find_element_by_class_name("jN-F5")

            time.sleep(1)

            searchbox.send_keys(group_name)
            searchbox.send_keys(Keys.ENTER)

            if (isFile):
                success = False

                while (success == False):
                    try:
                        iconBtn = self.driver.find_element_by_css_selector("span[data-icon='clip']")
                        iconBtn.click()

                        uploadFile = self.driver.find_element_by_css_selector('input[type=file]')
                        uploadFile.send_keys(imagePath)

                        self.time.sleep(2)

                        self.driver.find_element_by_css_selector(".bsmJe > div:nth-child(2)").send_keys(msg)
                        element = self.driver.find_element_by_css_selector("span[data-icon='send-light']")
                        element.click()

                        success = True
                    except:
                        success = False
            else:
                text = self.driver.find_element_by_class_name('_2S1VP')
                text.send_keys(msg)

                time.sleep(1)
                element = self.driver.find_element_by_class_name('_35EW6')
                element.click()

            messages = Messages(sender, group_name, msg, self.date_now, self.time_now)
            self.db.session.add(messages)
            self.db.session.commit()
            time.sleep(1)

    def cgroups(self, Messages, msg, time, selected_groups, Contacts_grouping, waitForButtonSend, sender, isFile,imagePath):
        for selected in selected_groups:

            contacts = Contacts_grouping.query.filter_by(group_name=selected)
            for number in contacts:
                self.driver.get('https://web.whatsapp.com/send?phone={}&text={}'.format(number.phone, msg))

                # WAIT FOR ELEMENT SEND BUTTON CAN BE CLICKED
                waitForButtonSend(self.driver)
                time.sleep(1)

                if (isFile):
                    success = False

                    while (success == False):
                        try:
                            iconBtn = self.driver.find_element_by_css_selector("span[data-icon='clip']")
                            iconBtn.click()

                            uploadFile = self.driver.find_element_by_css_selector('input[type=file]')
                            uploadFile.send_keys(imagePath)

                            self.time.sleep(2)

                            self.driver.find_element_by_css_selector(".bsmJe > div:nth-child(2)").send_keys(msg)
                            element = self.driver.find_element_by_css_selector("span[data-icon='send-light']")
                            element.click()

                            success = True
                        except:
                            success = False
                    else:
                        element = self.driver.find_element_by_class_name('_35EW6')
                        element.click()

                messages = Messages(sender, number.phone, msg, self.date_now, self.time_now)
                self.db.session.add(messages)
                self.db.session.commit()

                time.sleep(5)
        self.driver.close()