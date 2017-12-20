import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { HttpClientProvider } from '../../providers/http-client/http-client';
/**
 * Generated class for the SignUpPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-sign-up',
  templateUrl: 'sign-up.html',
})
export class SignUpPage {

  registerCredentials = { email: '',
                          password: '',
                          name:'',
                          phone:'',
                          country:'' };
  constructor(public navCtrl: NavController, public navParams: NavParams, public httpService: HttpClientProvider) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad SignUpPage');
  }

  public createAccount() {

  }

  public register() {
    let apiParams ={
        "email":this.registerCredentials.email,
        "password": this.registerCredentials.password,
        "phone_no": this.registerCredentials.phone,
        "first_name": this.registerCredentials.name.split(" ")[0],
        "last_name": this.registerCredentials.name.split(" ")[1] || '',
        "address": {
            "line1": "",
            "location": "",
            "city_or_village": "",
            "state": "",
            "country": "USA",
            "pin_code": null
        }
    }
    console.log(apiParams);
    this.httpService.postService('signup',apiParams).then((result) => {
        console.log(result);
    }, (err) => {
        console.log(err);
    });
  }

  showLoading() {
  }

  showError(text) {
  }

}
