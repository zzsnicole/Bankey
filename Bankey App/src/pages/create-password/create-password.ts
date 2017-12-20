import { EnterOtpPage } from './../enter-otp/enter-otp';
import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';

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

	createPasswordLabel = "Create a Password for your Bankey account";
	enteredPasscode = '';
	firstPassword = '';
	confirmPassword = ''

	constructor(public navCtrl: NavController, public navParams: NavParams) {
	}

	ionViewDidLoad() {
		console.log('ionViewDidLoad CreatePasswordPage');
	}

	digit(d) {
		this.enteredPasscode += '' + d;
		if (this.enteredPasscode.length == 4) {
			if (this.firstPassword == '') {
				this.createPasswordLabel = 'Re-enter your password again';
				this.firstPassword = this.enteredPasscode;
				this.enteredPasscode = '';
			} else {
				if (this.enteredPasscode != this.firstPassword) {
					this.createPasswordLabel = 'Please try again';
					this.enteredPasscode = '';
					this.firstPassword = '';
					this.confirmPassword = '';
				} else {
					this.navCtrl.push(EnterOtpPage);
					//this.createPasswordLabel = 'Password macthes';
				}
			}
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
