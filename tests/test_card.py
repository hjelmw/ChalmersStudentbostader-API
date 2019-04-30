import pytest
import card

def test_card_base():

    # empty HTML obj should return error
    assert(card.Card("", 0).get_card()["data"]["details"] == "Document is empty")

def test_card_available_doors():

    # Check parsing works for simple sample HTML obj
    sample_door_html = "<html><body><div><section><section><div class=\"lockCard\"><div><span>EB 80 Innerdörr</span></div><button onclick=\"UnlockEntranceDoor(123641);\"></button></div><>/section></section></div></body></html>"
    ref_sample_door_json = { "data": { 0: { "door": "EB 80 Innerdörr", "door_id": 123641 } },"status": "success"}

    card_available_door = card.Card(sample_door_html, 0, "door", "door_id").get_card()

    assert ( card_available_door == ref_sample_door_json )



def test_card_laundry_schedule():
    
    # Check parsing works for simple sample HTML obj
    sample_laundry_schedule_html = "<html><body><div><section><div><div><div><div><div><div><div>test</div></div></div></div></div></div</div></section></div></body></html>"
    ref_laundry_schedule_json = { 
        "data": { 0: { "door": "EB 80 Innerdörr", "door_id": 123641 } },"status": "success" }

    card_laundry_schedule = card.Card(sample_laundry_schedule_html, 1, "duration", "day", "machines", "street", "machine_id").get_card()
    assert(card_laundry_schedule == ref_laundry_schedule_json)

def test_card_laundry_available():

    # Check parsing works for simple sample HTML obj
    sample_door_html = "<html style=\"background-color:black\"><body> <div class=\"main-content\" style=\"position:relative;\"> <header class=\"header\" style=\"position:relative;\"> <div style=\"position:relative; z-index:1; max-width:90%;\"> <h1 id=\"lblCurrentLocation\" class=\"pageHeader\">Boka — F&#246;rsta lediga tid — Tv&#228;tt</h1> <div style=\"display:inline-block; white-space:normal\"></div> </div> <div id=\"headNavigationRight\" style=\"position:absolute; right:0; top:0; margin:1.2rem; z-index:2;/*display:none*/\"> </div> </header> <section class=\"bodySection\" tabindex=\"-1\"> <div id=\"content\" style=\"display:none; background-color:white\"> <p id=\"bookingMsg\" tabindex=\"-1\" role=\"alert\" aria-hidden=\"true\" style=\"font-size:0\">Bokning p&#229;g&#229;r.</p> <div class=\"bookingCard\"> <div> 00:00-02:00 </div> <div class=\"cardSmallFont\"> FRE 26 APR </div> <div style=\"padding:1rem\"><img src=\"/AptusPortal/Images/Booking/tvatt.png\" alt=\"\" /> </div> <div> Tv&#228;ttmaskin 1 o 2<br /> </div> <div class=\"cardSmallFont\"> Gibraltarg 82 Tv&#228;tt<br /><br /> </div> <button type=\"button\" onclick=\"DoBooking('/AptusPortal/CustomerBooking/BookFirstAvailable?passNo=0&amp;passDate=2019-04-26&amp;bookingGroupId=38'); return false;\" class=\"bookButton bookButtonFirstAvailable\" aria-label=\"Boka Tv&#228;ttmaskin 1 o 2 den 26 april 2019 00:00 Till 02:00\"> Boka </button> </div> <div class=\"bookingCard\"> <div> 00:00-02:00 </div> <div class=\"cardSmallFont\"> FRE 26 APR </div> <div style=\"padding:1rem\"><img src=\"/AptusPortal/Images/Booking/tvatt.png\" alt=\"\" /> </div> <div> Tv&#228;ttmaskin 3 o 4<br /> </div> <div class=\"cardSmallFont\"> Gibraltarg 82 Tv&#228;tt<br /><br /> </div> <button type=\"button\" onclick=\"DoBooking('/AptusPortal/CustomerBooking/BookFirstAvailable?passNo=0&amp;passDate=2019-04-26&amp;bookingGroupId=39'); return false;\" class=\"bookButton bookButtonFirstAvailable\" aria-label=\"Boka Tv&#228;ttmaskin 3 o 4 den 26 april 2019 00:00 Till 02:00\"> Boka </button> </div></div> <br /> </section> <footer class=\"footer\" style=\"position:fixed; bottom:0; width:100%; text-align:center; display:none\"> </footer> <a id=\"lastFocus\" href=\"javascript:void(0);\" style=\"line-height:none\" aria-label=\" \"></a> </div></body></html>"
    
    ref_laundry_available_json = { 
        "data": {
            0: {
                "bookingGroupId": "38",
                "date": "FRE 26 APR",
                "laundry_room": "Tvättmaskin 1 o 2",
                "passDate": "2019-04-26",
                "passNo": "0",
                "street": "Gibraltarg 82 Tvätt",
                "time": "00:00-02:00"
            },
            1: {
                "bookingGroupId": "39",
                "date": "FRE 26 APR",
                "laundry_room": "Tvättmaskin 3 o 4",
                "passDate": "2019-04-26",
                "passNo": "0",
                "street": "Gibraltarg 82 Tvätt",
                "time": "00:00-02:00"
            }
        },
        "status": "success"
        }

    card_laundry_bookings = card.Card(sample_door_html, 1, "time", "duration", "day", "machines", "street", "machine_id").get_card()
    assert(card_laundry_bookings == ref_laundry_available_json)

def test_card_invoice_list():
    