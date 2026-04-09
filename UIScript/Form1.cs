using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace FinalProject
{
	public partial class formMain : Form
	{
		public formMain()
		{
			InitializeComponent();
		}

		private void btnTestUser_Click(object sender, EventArgs e)
		{
			this.Hide();
			var form2 = new formTestUser();
			form2.ShowDialog();
			this.Close();
		}

		private void btnTestCase_Click(object sender, EventArgs e)
		{
			this.Hide();
			var form3 = new formTestCase();
			form3.ShowDialog();
			this.Close();
		}
	}
}
	

