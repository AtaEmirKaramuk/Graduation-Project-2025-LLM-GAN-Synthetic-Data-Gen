using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FinalProject
{
	public class settingsParser
	{
		public bool UseGpu { get; private set; }
		public bool UseZephyr { get; private set; }
		public bool UseDefault {  get; private set; }
		public string RunNumber { get; private set; }
		public string Url { get; private set; }
		public string Prompt { get; private set; }

		public void LoadFromFileArgos(string filePath)
		{
			if (!File.Exists(filePath))
				throw new FileNotFoundException("settings.py not found", filePath);

			var lines = File.ReadAllLines(filePath);

			foreach (var line in lines)
			{
				var trimmed = line.Trim();

				if (trimmed.StartsWith("USE_GPU ="))
					UseGpu = ParseBoolValue(trimmed);
				else if (trimmed.StartsWith("USE_ZEPHYR ="))
					UseZephyr = ParseBoolValue(trimmed);
				else if (trimmed.StartsWith("ALL_CASES ="))
					UseDefault = ParseBoolValue(trimmed);
				else if (trimmed.StartsWith("NUM_ZEPHYR_RUNS ="))
					RunNumber = ParseNumberValue(trimmed);
				else if (trimmed.StartsWith("URL ="))
							Url = ParseStringValue(trimmed);
			}
		}
		
		public void LoadUrlFileDelphi(string urlPath)
		{
			if (!File.Exists(urlPath)) throw new FileNotFoundException("settings.py not found", urlPath);
			
			var lines = File.ReadAllLines(urlPath);
			
			foreach (var line in lines)
			{
				var trimmed = line.Trim();

				if (trimmed.StartsWith("URL ="))
					Url = ParseStringValue(trimmed);
			}
		}

		public void LoadPromptFileDelphi(string promptPath)
		{
			if (!File.Exists(promptPath)) throw new FileNotFoundException("Prompt file not found", promptPath);

			var lines = File.ReadAllLines(promptPath);

			foreach (var line in lines)
			{
				var trimmed = line.Trim();

				if (trimmed.StartsWith("\"prompt\":"))
				{
					int colonIndex = trimmed.IndexOf(':');
					if (colonIndex != -1)
					{
						string valuePart = trimmed.Substring(colonIndex + 1).Trim();

						if (valuePart.StartsWith("\"") && valuePart.EndsWith("\""))
						{
							valuePart = valuePart.Substring(1, valuePart.Length - 2);
						}
						Prompt = valuePart;
						break;
					}
				}
			}
		}

		private bool ParseBoolValue(string line)
		{
			var value = line.Split('=')[1].Trim();
			return value.Equals("True", StringComparison.OrdinalIgnoreCase);
		}

		private string ParseNumberValue(string line)
		{
			var value = line.Split('=')[1].Trim();
			if (value.StartsWith(" ") && value.EndsWith(" ")) ;
			return value;
		}

		private string ParseStringValue(string line)
		{
			var value = line.Split('=')[1].Trim();
			// Remove surrounding quotes if present
			if (value.StartsWith("\"") && value.EndsWith("\""))
				return value.Substring(1, value.Length - 2);
			if (value.StartsWith("'") && value.EndsWith("'"))
				return value.Substring(1, value.Length - 2);
			return value;
		}
	}
}
