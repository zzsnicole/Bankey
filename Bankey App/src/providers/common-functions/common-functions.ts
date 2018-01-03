import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AlertController } from 'ionic-angular';
/*
  Generated class for the CommonFunctionsProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class CommonFunctionsProvider {

  constructor(public http: HttpClient,
              public alertCtrl: AlertController) {
    console.log('Hello CommonFunctionsProvider Provider');
  }

  showConfirm() {
   let confirm = this.alertCtrl.create({
     title: 'Use this lightsaber?',
     message: 'Do you agree to use this lightsaber to do good across the intergalactic galaxy?',
     buttons: [
       {
         text: 'Disagree',
         handler: () => {
           console.log('Disagree clicked');
         }
       },
       {
         text: 'Agree',
         handler: () => {
           console.log('Agree clicked');
         }
       }
     ]
   });
   confirm.present();
 }

 showAlert(alertText) {
   let alert = this.alertCtrl.create({
     title: 'Bankey!',
     subTitle: alertText,
     buttons: ['OK']
   });
   alert.present();
 }
}
