import { Component } from '@angular/core';
import {IonicPage, ModalController, NavController, NavParams} from 'ionic-angular';
import { Contacts, Contact, ContactField, ContactName } from '@ionic-native/contacts';
import {AddContactPage} from "../add-contact/add-contact";
import {EnterAmountPage} from "../enter-amount/enter-amount";
/**
 * Generated class for the ContactListPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-contact-list',
  templateUrl: 'contact-list.html',
})
export class ContactListPage {
  loadingModal:any;
  public allContacts: any = [];
  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              private contacts: Contacts,
              public modalCtrl:ModalController) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad ContactListPage');
    this.getAllContact();
  }

  getAllContact(){
      this.contacts.find(['displayName', 'name', 'phoneNumbers', 'emails'], {filter: "", multiple: true})
          .then(data => {
              console.log(data);
              this.allContacts = data.map((contact)=>{
                return {"name":contact.name["formatted"],
                        "phoneNumber":contact.phoneNumbers[0].value,
                        "photo":(contact.photos != null)?contact.photos[0].value:null};
              });
              console.log(this.allContacts);
      });
  }

  OpenAddContactModal(){
    //this.loadingModal = this.modalCtrl.create(AddContactPage);
    //this.loadingModal.present();
  }
  GoEnterAmount(){
    this.navCtrl.push(EnterAmountPage,{"send":true});
  }
}
