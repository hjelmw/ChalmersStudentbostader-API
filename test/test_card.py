import pytest
import card

def test_card_empty():
    # empty HTML obj should return error
    empty_html_card = card.Card("", 0)
    assert(empty_html_card.get_card()["status"] == "error")
    assert(empty_html_card.get_card()["data"]["details"] == "Document is empty")

    # empty xpath should also return error
    sample_html = "<html><body><div><h1>sample</h1></div></body></html>"
    invalid_html_card = card.Card(sample_html, 0, "door")
    assert(invalid_html_card.get_card()["status"] == "error")
    assert(invalid_html_card.get_card()["data"]["details"] == "xpath return empty. Check parameters")

    
def test_card_available_doors():

    with open(r"test\html\sample_available_doors.html", "r", encoding="utf-8") as f:
        sample_doors_html = f.read()

    ref_sample_door_json = {
        "data": {
            0: {
                "door": "EB 80 Innerdörr",
                "door_id": 123641
            },
            1: {
                "door": "EB 80 Ytterdörr",
                "door_id": 123640
            },
            2: {
                "door": "EB 82 Ytterdörr",
                "door_id": 123518
            },
            3: {
                "door": "EB 84 Ytterdörr",
                "door_id": 123596
            },
            4: {
                "door": "EB 86 Ytterdörr",
                "door_id": 123597
            },
            5: {
                "door": "EB 88 Ytterdörr",
                "door_id": 123599
            },
            6: {
                "door": "EB 90 Ytterdörr",
                "door_id": 123612
            },
            7: {
                "door": "EB 92 Ytterdörr",
                "door_id": 123613
            },
            8: {
                "door": "EB 94 Ytterdörr",
                "door_id": 123626
            }
        },
        "status": "success"
    }

    card_available_door = card.Card(sample_doors_html, 0, "door", "door_id").get_card()
    assert (card_available_door == ref_sample_door_json)


def test_card_laundry_schedule():
    with open(r"test\html\sample_schedule_laundry.html", "r", encoding="utf-8") as f:
        schedule_laundry_html = f.read()

    ref_schedule_laundry = {
        "data": {
            0: {
                "day": "ONS 1 MAJ",
                "duration": "13:00-16:00",
                "machine_id": 8434329,
                "machines": "Tvättstuga 10",
                "street": "EB 90 Tvättstuga 1-5"
            }
        },
        "status": "success"
    }

    card_available_laundry = card.Card(schedule_laundry_html, 1, "duration", "day", "machines", "street", "machine_id").get_card()
    assert(card_available_laundry == ref_schedule_laundry)



def test_card_laundry_available():
    
    with open(r"test\html\sample_available_laundry.html", "r", encoding="utf-8") as f:
        available_laundry_html = f.read()

    ref_available_laundry = {
        "data": {
            0: {
                "booking_params": { 
                    "bookingGroupId": "38",
                    "passDate": "2019-04-30",
                    "passNo": "1",
                },
                "date": "TIS 30 APR",
                "laundry_room": "Tvättmaskin 1 o 2",
                "street": "Gibraltarg 82 Tvätt",
                "time": "02:00-04:00"
            },
            1: {
                "booking_params": {
                    "bookingGroupId": "39",
                    "passDate": "2019-04-30",
                    "passNo": "1",
                },
                "date": "TIS 30 APR",
                "laundry_room": "Tvättmaskin 3 o 4",
                "street": "Gibraltarg 82 Tvätt",
                "time": "02:00-04:00"
            }
        },
        "status": "success"
    }

    card_available_laundry = card.Card(available_laundry_html, 2, "time", "date", "laundry_room", "street", "booking_params").get_card()
    assert(card_available_laundry == ref_available_laundry)

def test_card_avilista():
    
    with open(r"test\html\sample_avilista.html", "r", encoding="utf-8") as f:
        avilista_html = f.read()

    ref_avilista = {
        "data": {
            0: {
                "amount": "3 136 kr",
                "date_of_payment": "2019-04-30",
                "invoice": "Invoice May 2019",
                "invoice_status": "To pay at latest ",
                "ocr": 0000000000,
                "pdf_link": "https://www.chalmersstudentbostader.se//link1"
            },
            1: {
                "amount": "5 567 kr",
                "date_of_payment": "2019-03-31",
                "invoice": "Invoice April 2019",
                "invoice_status": "paid ",
                "ocr": 1234567890,
                "pdf_link": "https://www.chalmersstudentbostader.se//link2"
            },
            2: {
                "amount": "336 kr",
                "date_of_payment": "2019-02-28",
                "invoice": "Invoice March 2019",
                "invoice_status": "paid ",
                "ocr": 2345678901,
                "pdf_link": "https://www.chalmersstudentbostader.se//link3"
            },
            3: {
                "amount": "36 kr",
                "date_of_payment": "2019-01-31",
                "invoice": "Invoice February 2019",
                "invoice_status": "paid ",
                "ocr": 3456789012,
                "pdf_link": "https://www.chalmersstudentbostader.se//link4"
            }
        },
        "status" : "success" 
    }

    card_avilista = card.Card(avilista_html, 3, "invoice", "invoice_status", "amount", "date_of_payment", "ocr", "pdf_link").get_card()
    assert(card_avilista == ref_avilista)

def test_card_book():
    
    with open(r"test\html\sample_booking_result.html", "r", encoding="utf-8") as f:
        book_html = f.read()
    card_book = card.Card(book_html, 4, "booking_result").get_card()

    ref_avilista = {
        "data": {
            0: {
                "booking_result": "Ditt valda testpass är bokat."
            }
        },
        "status": "success"
    }

    assert(card_book == ref_avilista)

def test_card_news_omradesnyhet():
     
    with open(r"test\html\sample_news_omradesnyhet.html", "r", encoding="utf-8") as f:
        news_omradesnyhet_html = f.read()
    

    ref_omradesnyhet = {
        "data": {
            0: {
                "news_date": "9 april, 2019",
                "news_headline": "testrubrik1",
                "news_link": "https://www.chalmersstudentbostader.se/2019/linknyhet1/",
                "news_text": "Testnyhet1"
            },
            1: {
                "news_date": "26 november, 2018",
                "news_headline": "testrubrik2",
                "news_link": "https://www.chalmersstudentbostader.se/2018/linknyhet2/",
                "news_text": "Testnyhet2"
            },
            2: {
                "news_date": "19 juli, 2017",
                "news_headline": "testrubrik3",
                "news_link": "https://www.chalmersstudentbostader.se/2017/linknyhet3/",
                "news_text": "Testnyhet3"
            }
        },
        "status": "success"
    }

    card_omradesnyhet = card.Card(news_omradesnyhet_html, 5, "news_date", "news_headline", "news_text", "news_link").get_card()
    assert(card_omradesnyhet == ref_omradesnyhet)

def test_card_news_nyheter():
     
    with open(r"test\html\sample_news_nyheter.html", "r", encoding="utf-8") as f:
        news_nyheter_html = f.read()
    

    ref_nyheter = {
        "data": {
            0: {
                "news_date": "1 april, 2019",
                "news_headline": "Nyhet1",
                "news_link": "https://www.chalmersstudentbostader.se/2019/linknyhet1/",
                "news_text": "lorem ipsum text text"
            },
            1: {
                "news_date": "15 mars, 2019",
                "news_headline": "Nyhet2",
                "news_link": "https://www.chalmersstudentbostader.se/2019/linknyhet2/",
                "news_text": "ipsum lorem text text"
            },
            2: {
                "news_date": "18 december, 2018",
                "news_headline": "Nyhet3",
                "news_link": "https://www.chalmersstudentbostader.se/2018/linknyhet3/",
                "news_text": "text lorem text ipsum"
            },
            3: {
                "news_date": "17 oktober, 2018",
                "news_headline": "Nyhet4",
                "news_link": "https://www.chalmersstudentbostader.se/2018/linknyhet4/",
                "news_text": "lorem text ipsum text"
            }
        },
        "status": "success"
    }

    card_nyheter = card.Card(news_nyheter_html, 5, "news_date", "news_headline", "news_text", "news_link").get_card()
    assert(card_nyheter == ref_nyheter)