from src.data_processor import EmailDataLoader, EmailBodyGenerator
from src.email_sender import EmailConfigLoader, EmailSender

if __name__ == '__main__':
    """Main entry point for sending a purchase confirmation email with attachment."""
    
    config_loader = EmailConfigLoader()
    config = config_loader.load_config('config.yaml')

    data_loader = EmailDataLoader()
    purchase_data = data_loader.load_data(config['email_config']['purchase_data'])

    email_body_generator = EmailBodyGenerator(config['email_config']['email_template'])
    email_body = email_body_generator.generate(purchase_data)

    email_sender = EmailSender(
        sender_email=config['email_config']['smtp']['sender'],
        sender_password=config['email_config']['smtp']['password'],
        config_file='config.yaml'
    )
    
    email_sender.send_email(
        recipient=config['email_config']['recipient'],
        email_body=email_body,
        attachment_path=config['email_config']['attachment'],
        subject=config['email_config']['subject']  
    )
