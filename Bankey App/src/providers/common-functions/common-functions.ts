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

  showConfirm(title,button1,button2,alertText) {
    return new Promise((resolve,reject) => {
        let confirm = this.alertCtrl.create({
            title: title,
            message: alertText,
            buttons: [
                {
                    text: button1,
                    handler: () => {
                        console.log('Disagree clicked');
                        resolve(button1);
                    }
                },
                {
                    text: button2,
                    handler: () => {
                        console.log('Agree clicked');
                        resolve(button2);
                    }
                }
            ]
        });
        confirm.present();
    });
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
