import { PersonalDetailsPage } from './../personal-details/personal-details';
import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import {CommonFunctionsProvider} from "../../providers/common-functions/common-functions";
import {HttpClientProvider} from "../../providers/http-client/http-client";

/**
 * Generated class for the CreatePasswordPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
	selector: 'page-create-password',
	templateUrl: 'create-password.html',
})
export class CreatePasswordPage {

	createPasswordLabel = "Create a passcode for your Bankey account";
	enteredPasscode = '';
	firstPassword = '';
	confirmPassword = '';
    isPassChange = false;
	constructor(public navCtrl: NavController,
				public navParams: NavParams,
				public commonFn: CommonFunctionsProvider,
				public httpClient: HttpClientProvider) {
	}

	ionViewDidLoad() {
		console.log('ionViewDidLoad CreatePasswordPage');
        this.isPassChange = this.navParams.get("pass_change");
        if(this.isPassChange){
            this.createPasswordLabel = "reset a passcode for your Bankey account";
		}
	}

	digit(d) {
		if(d == -1){
				this.delete();
		}else{
			  this.enteredPasscode += '' + d;
		}
		if (this.enteredPasscode.length == 4) {
			if (this.firstPassword == '') {
				this.createPasswordLabel = 'Re-enter your passcode again';
				this.firstPassword = this.enteredPasscode;
				this.enteredPasscode = '';
			} else {
				if (this.enteredPasscode != this.firstPassword) {
					this.createPasswordLabel = 'Please try again';
					this.enteredPasscode = '';
					this.firstPassword = '';
					this.confirmPassword = '';
				} else {
					this.setPassword();

				}
			}
		}
	}

  setPassword() {
		if(this.isPassChange){
            this.httpClient.postService('forgotpassword/',{"mobile_number":localStorage.mobileNumber,
				"password":this.enteredPasscode }).then((result:any) => {
                console.log(result);
                if(result.success){
                    this.navCtrl.remove(2,1);
                    this.navCtrl.pop();
                }else{
                    this.commonFn.showAlert(result.message);
                }
            }, (err) => {
                console.log(err);
            });

		}else {
          this.navCtrl.push(PersonalDetailsPage,{"password_":this.enteredPasscode});
	    }
  }

	delete() {
		this.enteredPasscode = this.enteredPasscode.slice(0, -1);

	}

	clear() {
		this.enteredPasscode = "";
	};

	goBack(){
		this.navCtrl.pop();
	}

}
