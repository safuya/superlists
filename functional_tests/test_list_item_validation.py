from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
import unittest
from time import sleep


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Ellie goes to the home page and accidentally tries to submit an
        # empty list item. She hits Enter on the empty self.browser.find_element_by_id('id_new_item')
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # The homepage refreshes and there is an error message saying that the
        # list items cannot be blank
        with self.wait_for_page_load(timeout=10):
            self.assertEqual(
                    self.browser.find_element_by_class_name('has-error').text,
                    "You can't have an empty list item",
                    "First attempt at blank input not returning error."
            )

        # She tries again with some text for the new item which now works
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table('1: Buy milk')

        # Perversely she now decides to submit a second blank list item
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # She receives a similar warning on the list page
        with self.wait_for_page_load(timeout=10):
            self.assertEqual(
                    self.browser.find_element_by_class_name('has-error').text,
                    "You can't have an empty list item",
                    "Second attempt at blank input not returning error."
            )

        # And she can correct it by filling some text in
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        with self.wait_for_page_load(timeout=10):
            self.check_for_row_in_list_table('1: Buy milk')
            self.check_for_row_in_list_table('2: Make tea')


if __name__ == '__main__':
    unittest.main()

