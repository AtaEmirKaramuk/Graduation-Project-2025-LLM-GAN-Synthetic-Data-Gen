namespace FinalProject
{
	partial class formTestUser
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(formTestUser));
            this.btnCreateTestUsers = new System.Windows.Forms.Button();
            this.grpSettings = new System.Windows.Forms.GroupBox();
            this.panelLLM = new System.Windows.Forms.Panel();
            this.radioPrompt = new System.Windows.Forms.RadioButton();
            this.radioURL = new System.Windows.Forms.RadioButton();
            this.label3 = new System.Windows.Forms.Label();
            this.chbxUseLLM = new System.Windows.Forms.CheckBox();
            this.label2 = new System.Windows.Forms.Label();
            this.panelURL = new System.Windows.Forms.Panel();
            this.label1 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.txtURL = new System.Windows.Forms.TextBox();
            this.btnReturn = new System.Windows.Forms.Button();
            this.btnSaveSettings = new System.Windows.Forms.Button();
            this.button1 = new System.Windows.Forms.Button();
            this.panelPrompt = new System.Windows.Forms.Panel();
            this.richTextPrompt = new System.Windows.Forms.RichTextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.grpSettings.SuspendLayout();
            this.panelLLM.SuspendLayout();
            this.panelURL.SuspendLayout();
            this.panelPrompt.SuspendLayout();
            this.SuspendLayout();
            // 
            // btnCreateTestUsers
            // 
            this.btnCreateTestUsers.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(162)));
            this.btnCreateTestUsers.Location = new System.Drawing.Point(368, 104);
            this.btnCreateTestUsers.Name = "btnCreateTestUsers";
            this.btnCreateTestUsers.Size = new System.Drawing.Size(314, 99);
            this.btnCreateTestUsers.TabIndex = 10;
            this.btnCreateTestUsers.Text = "Create Test Data";
            this.btnCreateTestUsers.UseVisualStyleBackColor = true;
            this.btnCreateTestUsers.Click += new System.EventHandler(this.btnCreateTestUsers_Click);
            // 
            // grpSettings
            // 
            this.grpSettings.Controls.Add(this.panelLLM);
            this.grpSettings.Controls.Add(this.chbxUseLLM);
            this.grpSettings.Controls.Add(this.label2);
            this.grpSettings.Location = new System.Drawing.Point(12, 12);
            this.grpSettings.Name = "grpSettings";
            this.grpSettings.Size = new System.Drawing.Size(348, 282);
            this.grpSettings.TabIndex = 12;
            this.grpSettings.TabStop = false;
            this.grpSettings.Text = "Settings";
            // 
            // panelLLM
            // 
            this.panelLLM.Controls.Add(this.radioPrompt);
            this.panelLLM.Controls.Add(this.radioURL);
            this.panelLLM.Controls.Add(this.label3);
            this.panelLLM.Location = new System.Drawing.Point(0, 68);
            this.panelLLM.Name = "panelLLM";
            this.panelLLM.Size = new System.Drawing.Size(347, 219);
            this.panelLLM.TabIndex = 5;
            // 
            // radioPrompt
            // 
            this.radioPrompt.AutoSize = true;
            this.radioPrompt.Location = new System.Drawing.Point(8, 53);
            this.radioPrompt.Name = "radioPrompt";
            this.radioPrompt.Size = new System.Drawing.Size(80, 17);
            this.radioPrompt.TabIndex = 6;
            this.radioPrompt.TabStop = true;
            this.radioPrompt.Text = "Use Prompt";
            this.radioPrompt.UseVisualStyleBackColor = true;
            this.radioPrompt.CheckedChanged += new System.EventHandler(this.radioPrompt_CheckedChanged);
            // 
            // radioURL
            // 
            this.radioURL.AutoSize = true;
            this.radioURL.Location = new System.Drawing.Point(8, 30);
            this.radioURL.Name = "radioURL";
            this.radioURL.Size = new System.Drawing.Size(86, 17);
            this.radioURL.TabIndex = 5;
            this.radioURL.TabStop = true;
            this.radioURL.Text = "Use Website";
            this.radioURL.UseVisualStyleBackColor = true;
            this.radioURL.CheckedChanged += new System.EventHandler(this.radioURL_CheckedChanged);
            // 
            // label3
            // 
            this.label3.Location = new System.Drawing.Point(5, 6);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(342, 20);
            this.label3.TabIndex = 4;
            this.label3.Text = "Do you wish to use a Website URL to generate data or give your own promt describi" +
    "ng the data.";
            // 
            // chbxUseLLM
            // 
            this.chbxUseLLM.AutoSize = true;
            this.chbxUseLLM.Location = new System.Drawing.Point(8, 39);
            this.chbxUseLLM.Name = "chbxUseLLM";
            this.chbxUseLLM.Size = new System.Drawing.Size(69, 17);
            this.chbxUseLLM.TabIndex = 4;
            this.chbxUseLLM.Text = "Use LLM";
            this.chbxUseLLM.UseVisualStyleBackColor = true;
            this.chbxUseLLM.CheckedChanged += new System.EventHandler(this.chbxUseLLM_CheckedChanged);
            // 
            // label2
            // 
            this.label2.Location = new System.Drawing.Point(5, 16);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(342, 20);
            this.label2.TabIndex = 3;
            this.label2.Text = "If you wish to use the LLM functionality check the \"Use LLM\" option.\r\n\r\n";
            // 
            // panelURL
            // 
            this.panelURL.Controls.Add(this.label1);
            this.panelURL.Controls.Add(this.label4);
            this.panelURL.Controls.Add(this.txtURL);
            this.panelURL.Location = new System.Drawing.Point(12, 151);
            this.panelURL.Name = "panelURL";
            this.panelURL.Size = new System.Drawing.Size(347, 148);
            this.panelURL.TabIndex = 5;
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(5, 9);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(336, 28);
            this.label1.TabIndex = 1;
            this.label1.Text = "Please enter a URL for the website you wish the generate user data for.";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(6, 45);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(32, 13);
            this.label4.TabIndex = 2;
            this.label4.Text = "URL:";
            // 
            // txtURL
            // 
            this.txtURL.Location = new System.Drawing.Point(40, 42);
            this.txtURL.Name = "txtURL";
            this.txtURL.Size = new System.Drawing.Size(301, 20);
            this.txtURL.TabIndex = 3;
            // 
            // btnReturn
            // 
            this.btnReturn.BackColor = System.Drawing.SystemColors.ControlLightLight;
            this.btnReturn.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(162)));
            this.btnReturn.Location = new System.Drawing.Point(368, 16);
            this.btnReturn.Name = "btnReturn";
            this.btnReturn.Size = new System.Drawing.Size(158, 85);
            this.btnReturn.TabIndex = 13;
            this.btnReturn.Text = "Return";
            this.btnReturn.UseVisualStyleBackColor = false;
            this.btnReturn.Click += new System.EventHandler(this.btnReturn_Click);
            // 
            // btnSaveSettings
            // 
            this.btnSaveSettings.BackColor = System.Drawing.SystemColors.ControlLightLight;
            this.btnSaveSettings.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(162)));
            this.btnSaveSettings.Location = new System.Drawing.Point(528, 16);
            this.btnSaveSettings.Name = "btnSaveSettings";
            this.btnSaveSettings.Size = new System.Drawing.Size(154, 85);
            this.btnSaveSettings.TabIndex = 14;
            this.btnSaveSettings.Text = "Save Settings";
            this.btnSaveSettings.UseVisualStyleBackColor = false;
            this.btnSaveSettings.Click += new System.EventHandler(this.btnSaveSettings_Click);
            // 
            // button1
            // 
            this.button1.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(162)));
            this.button1.Location = new System.Drawing.Point(368, 209);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(320, 85);
            this.button1.TabIndex = 16;
            this.button1.Text = "Continue to Test Case Generation";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // panelPrompt
            // 
            this.panelPrompt.Controls.Add(this.richTextPrompt);
            this.panelPrompt.Controls.Add(this.label5);
            this.panelPrompt.Controls.Add(this.label6);
            this.panelPrompt.Location = new System.Drawing.Point(12, 151);
            this.panelPrompt.Name = "panelPrompt";
            this.panelPrompt.Size = new System.Drawing.Size(347, 148);
            this.panelPrompt.TabIndex = 17;
            // 
            // richTextPrompt
            // 
            this.richTextPrompt.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.richTextPrompt.Location = new System.Drawing.Point(55, 42);
            this.richTextPrompt.Name = "richTextPrompt";
            this.richTextPrompt.Size = new System.Drawing.Size(286, 96);
            this.richTextPrompt.TabIndex = 3;
            this.richTextPrompt.Text = "";
            // 
            // label5
            // 
            this.label5.Location = new System.Drawing.Point(5, 9);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(336, 28);
            this.label5.TabIndex = 1;
            this.label5.Text = "Please make sure the prompt you are entering is in a similar fashion to the promp" +
    "t below. Prompts not in the correct form can lead to the algorithm working poorl" +
    "y.";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(6, 45);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(43, 13);
            this.label6.TabIndex = 2;
            this.label6.Text = "Prompt:";
            // 
            // formTestUser
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(694, 311);
            this.Controls.Add(this.panelPrompt);
            this.Controls.Add(this.panelURL);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.btnSaveSettings);
            this.Controls.Add(this.btnReturn);
            this.Controls.Add(this.grpSettings);
            this.Controls.Add(this.btnCreateTestUsers);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "formTestUser";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "DelphiGEN";
            this.grpSettings.ResumeLayout(false);
            this.grpSettings.PerformLayout();
            this.panelLLM.ResumeLayout(false);
            this.panelLLM.PerformLayout();
            this.panelURL.ResumeLayout(false);
            this.panelURL.PerformLayout();
            this.panelPrompt.ResumeLayout(false);
            this.panelPrompt.PerformLayout();
            this.ResumeLayout(false);

		}

		#endregion
		private System.Windows.Forms.Button btnCreateTestUsers;
		private System.Windows.Forms.GroupBox grpSettings;
		private System.Windows.Forms.Button btnReturn;
		private System.Windows.Forms.Button btnSaveSettings;
		private System.Windows.Forms.CheckBox chbxUseLLM;
		private System.Windows.Forms.Label label2;
		private System.Windows.Forms.Label label1;
		private System.Windows.Forms.Label label4;
		private System.Windows.Forms.TextBox txtURL;
		private System.Windows.Forms.Panel panelURL;
		private System.Windows.Forms.Panel panelLLM;
		private System.Windows.Forms.Label label3;
		private System.Windows.Forms.RadioButton radioPrompt;
		private System.Windows.Forms.RadioButton radioURL;
		private System.Windows.Forms.Button button1;
		private System.Windows.Forms.Panel panelPrompt;
		private System.Windows.Forms.Label label5;
		private System.Windows.Forms.Label label6;
		private System.Windows.Forms.RichTextBox richTextPrompt;
	}
}