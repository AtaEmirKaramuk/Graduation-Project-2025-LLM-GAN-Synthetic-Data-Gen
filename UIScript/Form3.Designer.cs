namespace FinalProject
{
	partial class formTestCase
	{
		/// <summary>
		/// Required designer variable.
		/// </summary>
		private System.ComponentModel.IContainer components = null;

		/// <summary>
		/// Clean up any resources being used.
		/// </summary>
		/// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
		protected override void Dispose(bool disposing)
		{
			if (disposing && (components != null))
			{
				components.Dispose();
			}
			base.Dispose(disposing);
		}

		#region Windows Form Designer generated code

		/// <summary>
		/// Required method for Designer support - do not modify
		/// the contents of this method with the code editor.
		/// </summary>
		private void InitializeComponent()
		{
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(formTestCase));
            this.grpSettings = new System.Windows.Forms.GroupBox();
            this.chbxUseDefault = new System.Windows.Forms.CheckBox();
            this.label4 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.cbxLLM = new System.Windows.Forms.ComboBox();
            this.chbxUseLLM = new System.Windows.Forms.CheckBox();
            this.label2 = new System.Windows.Forms.Label();
            this.lblInstruction = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.lblURL = new System.Windows.Forms.Label();
            this.txtURL = new System.Windows.Forms.TextBox();
            this.chbxUseGPU = new System.Windows.Forms.CheckBox();
            this.btnCreateTestCase = new System.Windows.Forms.Button();
            this.btnAutomate = new System.Windows.Forms.Button();
            this.btnReturn = new System.Windows.Forms.Button();
            this.btnSaveSettings = new System.Windows.Forms.Button();
            this.grpSettings.SuspendLayout();
            this.SuspendLayout();
            // 
            // grpSettings
            // 
            this.grpSettings.Controls.Add(this.chbxUseDefault);
            this.grpSettings.Controls.Add(this.label4);
            this.grpSettings.Controls.Add(this.label3);
            this.grpSettings.Controls.Add(this.cbxLLM);
            this.grpSettings.Controls.Add(this.chbxUseLLM);
            this.grpSettings.Controls.Add(this.label2);
            this.grpSettings.Controls.Add(this.lblInstruction);
            this.grpSettings.Controls.Add(this.label1);
            this.grpSettings.Controls.Add(this.lblURL);
            this.grpSettings.Controls.Add(this.txtURL);
            this.grpSettings.Controls.Add(this.chbxUseGPU);
            this.grpSettings.Location = new System.Drawing.Point(12, 12);
            this.grpSettings.Name = "grpSettings";
            this.grpSettings.Size = new System.Drawing.Size(348, 282);
            this.grpSettings.TabIndex = 0;
            this.grpSettings.TabStop = false;
            this.grpSettings.Text = "Settings";
            // 
            // chbxUseDefault
            // 
            this.chbxUseDefault.AutoSize = true;
            this.chbxUseDefault.Location = new System.Drawing.Point(6, 144);
            this.chbxUseDefault.Name = "chbxUseDefault";
            this.chbxUseDefault.Size = new System.Drawing.Size(82, 17);
            this.chbxUseDefault.TabIndex = 8;
            this.chbxUseDefault.Text = "Use Default";
            this.chbxUseDefault.UseVisualStyleBackColor = true;
            // 
            // label4
            // 
            this.label4.Location = new System.Drawing.Point(3, 112);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(342, 26);
            this.label4.TabIndex = 7;
            this.label4.Text = "If you wish to include the default test case dataset in test check the \"Use Defau" +
    "lt\" option";
            // 
            // label3
            // 
            this.label3.Location = new System.Drawing.Point(3, 164);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(342, 20);
            this.label3.TabIndex = 6;
            this.label3.Text = "Please select how many times you would like to run the LLM";
            // 
            // cbxLLM
            // 
            this.cbxLLM.FormattingEnabled = true;
            this.cbxLLM.Items.AddRange(new object[] {
            "1",
            "2",
            "3",
            "4",
            "5"});
            this.cbxLLM.Location = new System.Drawing.Point(4, 187);
            this.cbxLLM.Name = "cbxLLM";
            this.cbxLLM.Size = new System.Drawing.Size(42, 21);
            this.cbxLLM.TabIndex = 5;
            // 
            // chbxUseLLM
            // 
            this.chbxUseLLM.AutoSize = true;
            this.chbxUseLLM.Location = new System.Drawing.Point(6, 92);
            this.chbxUseLLM.Name = "chbxUseLLM";
            this.chbxUseLLM.Size = new System.Drawing.Size(69, 17);
            this.chbxUseLLM.TabIndex = 4;
            this.chbxUseLLM.Text = "Use LLM";
            this.chbxUseLLM.UseVisualStyleBackColor = true;
            // 
            // label2
            // 
            this.label2.Location = new System.Drawing.Point(3, 69);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(342, 20);
            this.label2.TabIndex = 3;
            this.label2.Text = "If you wish to use the LLM functionality check the \"Use LLM\" option.\r\n";
            // 
            // lblInstruction
            // 
            this.lblInstruction.Location = new System.Drawing.Point(1, 211);
            this.lblInstruction.Name = "lblInstruction";
            this.lblInstruction.Size = new System.Drawing.Size(339, 48);
            this.lblInstruction.TabIndex = 1;
            this.lblInstruction.Text = "If you wish to generate a contextual test case please enter the URL to the websit" +
    "e you wish to train the model on. \r\nIf there are no URL\'s entered the model will" +
    " be non-contextual.";
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(3, 16);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(339, 30);
            this.label1.TabIndex = 2;
            this.label1.Text = "If you have a NVIDIA GPU that supports CUDA and wish to use that capability check" +
    " the \"Use GPU\" option.\r\n";
            // 
            // lblURL
            // 
            this.lblURL.AutoSize = true;
            this.lblURL.Location = new System.Drawing.Point(6, 259);
            this.lblURL.Name = "lblURL";
            this.lblURL.Size = new System.Drawing.Size(32, 13);
            this.lblURL.TabIndex = 2;
            this.lblURL.Text = "URL:";
            // 
            // txtURL
            // 
            this.txtURL.Location = new System.Drawing.Point(44, 256);
            this.txtURL.Name = "txtURL";
            this.txtURL.Size = new System.Drawing.Size(301, 20);
            this.txtURL.TabIndex = 3;
            this.txtURL.TextChanged += new System.EventHandler(this.txtURL_TextChanged);
            // 
            // chbxUseGPU
            // 
            this.chbxUseGPU.AutoSize = true;
            this.chbxUseGPU.Location = new System.Drawing.Point(6, 49);
            this.chbxUseGPU.Name = "chbxUseGPU";
            this.chbxUseGPU.Size = new System.Drawing.Size(71, 17);
            this.chbxUseGPU.TabIndex = 1;
            this.chbxUseGPU.Text = "Use GPU";
            this.chbxUseGPU.UseVisualStyleBackColor = true;
            // 
            // btnCreateTestCase
            // 
            this.btnCreateTestCase.BackColor = System.Drawing.SystemColors.ControlLightLight;
            this.btnCreateTestCase.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(162)));
            this.btnCreateTestCase.Location = new System.Drawing.Point(365, 111);
            this.btnCreateTestCase.Name = "btnCreateTestCase";
            this.btnCreateTestCase.Size = new System.Drawing.Size(317, 92);
            this.btnCreateTestCase.TabIndex = 4;
            this.btnCreateTestCase.Text = "Save Settings and Create Test Cases";
            this.btnCreateTestCase.UseVisualStyleBackColor = false;
            this.btnCreateTestCase.Click += new System.EventHandler(this.btnCreateTestCase_Click);
            // 
            // btnAutomate
            // 
            this.btnAutomate.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(162)));
            this.btnAutomate.Location = new System.Drawing.Point(365, 209);
            this.btnAutomate.Name = "btnAutomate";
            this.btnAutomate.Size = new System.Drawing.Size(317, 85);
            this.btnAutomate.TabIndex = 5;
            this.btnAutomate.Text = "Automate";
            this.btnAutomate.UseVisualStyleBackColor = true;
            this.btnAutomate.Click += new System.EventHandler(this.btnAutomate_Click);
            // 
            // btnReturn
            // 
            this.btnReturn.BackColor = System.Drawing.SystemColors.ControlLightLight;
            this.btnReturn.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(162)));
            this.btnReturn.Location = new System.Drawing.Point(366, 20);
            this.btnReturn.Name = "btnReturn";
            this.btnReturn.Size = new System.Drawing.Size(158, 85);
            this.btnReturn.TabIndex = 14;
            this.btnReturn.Text = "Return";
            this.btnReturn.UseVisualStyleBackColor = false;
            this.btnReturn.Click += new System.EventHandler(this.btnReturn_Click);
            // 
            // btnSaveSettings
            // 
            this.btnSaveSettings.BackColor = System.Drawing.SystemColors.ControlLightLight;
            this.btnSaveSettings.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(162)));
            this.btnSaveSettings.Location = new System.Drawing.Point(530, 20);
            this.btnSaveSettings.Name = "btnSaveSettings";
            this.btnSaveSettings.Size = new System.Drawing.Size(152, 85);
            this.btnSaveSettings.TabIndex = 15;
            this.btnSaveSettings.Text = "Save Settings";
            this.btnSaveSettings.UseVisualStyleBackColor = false;
            this.btnSaveSettings.Click += new System.EventHandler(this.btnSaveSettings_Click);
            // 
            // formTestCase
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(694, 311);
            this.Controls.Add(this.btnSaveSettings);
            this.Controls.Add(this.btnReturn);
            this.Controls.Add(this.btnAutomate);
            this.Controls.Add(this.btnCreateTestCase);
            this.Controls.Add(this.grpSettings);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "formTestCase";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "ArgosQA";
            this.grpSettings.ResumeLayout(false);
            this.grpSettings.PerformLayout();
            this.ResumeLayout(false);

		}

		#endregion

		private System.Windows.Forms.GroupBox grpSettings;
		private System.Windows.Forms.Label lblInstruction;
		private System.Windows.Forms.Label lblURL;
		private System.Windows.Forms.TextBox txtURL;
		private System.Windows.Forms.Button btnCreateTestCase;
		private System.Windows.Forms.Button btnAutomate;
		private System.Windows.Forms.Label label1;
		private System.Windows.Forms.CheckBox chbxUseGPU;
		private System.Windows.Forms.CheckBox chbxUseLLM;
		private System.Windows.Forms.Label label2;
		private System.Windows.Forms.Button btnReturn;
		private System.Windows.Forms.Button btnSaveSettings;
		private System.Windows.Forms.Label label3;
		private System.Windows.Forms.ComboBox cbxLLM;
		private System.Windows.Forms.CheckBox chbxUseDefault;
		private System.Windows.Forms.Label label4;
	}
}