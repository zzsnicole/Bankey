import { PersonalDetailsPage } from './../personal-details/personal-details';
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

	createPasswordLabel = "Create a passcode for your Bankey account";
	enteredPasscode = '';
	firstPassword = '';
	confirmPassword = ''

	constructor(public navCtrl: NavController, public navParams: NavParams) {
	}

	ionViewDidLoad() {
		console.log('ionViewDidLoad CreatePasswordPage');
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
          this.navCtrl.push(PersonalDetailsPage,{"password_":this.enteredPasscode});
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
