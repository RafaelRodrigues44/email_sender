import os
import smtplib
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header

class EmailConfigLoader:
    """Class responsible for loading email configuration from a YAML file."""

    @staticmethod
    def load_config(config_file):
        """Loads email configuration from a specified YAML file.

        Args:
            config_file (str): The path to the YAML configuration file.

        Returns:
            dict: The email configuration loaded from the file, containing SMTP server settings,
                  sender details, recipient details, and any other relevant email parameters.
        """
        with open(config_file, 'r', encoding='utf-8') as file:  
            config = yaml.safe_load(file)
        return config 

class EmailSender:
    """Class responsible for sending emails with attachments."""

    def __init__(self, sender_email, sender_password, config_file):
        """Initializes the EmailSender with sender credentials and loads email configuration.

        Args:
            sender_email (str): The email address of the sender.
            sender_password (str): The password for the sender's email account.
            config_file (str): The path to the YAML configuration file that contains email settings.
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.config = EmailConfigLoader.load_config(config_file)

    def send_email(self, recipient, email_body, attachment_path, subject):
        """Sends an email with an optional attachment to the specified recipient.

        Args:
            recipient (str): The email address of the recipient.
            email_body (str): The HTML body of the email.
            attachment_path (str): The file path to the attachment (if any). If None, no attachment is sent.
            subject (str): The subject of the email.

        Raises:
            Exception: If there is an error during the SMTP connection or email sending process.

        Prints:
            A success message if the email is sent successfully or an error message if it fails.
        """
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = recipient
        message['Subject'] = Header(subject, 'utf-8')

        message.attach(MIMEText(email_body, 'html', 'utf-8'))

        if attachment_path:
            if os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
                    message.attach(part)

        smtp_server = self.config['email_config']['smtp']['server']
        smtp_port = self.config['email_config']['smtp']['port']

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, recipient, message.as_string())
            server.quit()
            print(f"E-mail enviado com sucesso para {recipient}.")
        except Exception as e:
            print(f"Falha ao enviar o e-mail: {str(e)}")
