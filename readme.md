# Todo List Application with GraphQL and Stripe

Welcome to the Todo List Application! This project demonstrates a web app for managing tasks, built with Flask, GraphQL, and integrated with Stripe for payment processing. The app also includes authentication via Keycloak.

## Features

- **Task Management**: Create, edit, and delete tasks.
- **GraphQL API**: Fetch tasks and perform mutations using GraphQL.
- **Stripe Integration**: Payment processing with Stripe.
- **Keycloak Authentication**: Secure authentication with Keycloak.

## Project Structure

- **`app.py`**: The main application file with Flask routes and GraphQL schema definitions.
- **`config.py`**: Configuration settings for the application, including Keycloak settings.
- **`database.py`**: SQLAlchemy models and GraphQL schema for task management.
- **`index.html`**: Main page for displaying tasks and adding new ones.
- **`todolist.html`**: Extended HTML template for a more styled todo list page.
- **`edit.html`**: Page for editing existing tasks.

## Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the root directory and add your Stripe and Keycloak credentials:

   ```env
   STRIPE_API_KEY=your_stripe_api_key
   KEYCLOAK_SERVER_URL=http://localhost:8080/auth
   KEYCLOAK_CLIENT_ID=test-web-app
   KEYCLOAK_REALM_NAME=Gaurav
   KEYCLOAK_CLIENT_SECRET=OQ3AYXHn6jr91CPIiWAQdTH2slYinARo
   ```

## Keycloak Setup

To activate Keycloak and configure it for your application, follow these steps:

1. **Download and Run Keycloak**

   Download Keycloak from the [official website](https://www.keycloak.org/downloads). Extract the downloaded file and navigate to the Keycloak directory. Start Keycloak with the following command:

   ```bash
   ./bin/standalone.sh
   ```

   Keycloak will be accessible at `http://localhost:8080`.

2. **Create a Realm**

   - Go to the Keycloak admin console at `http://localhost:8080/auth/admin/`.
   - Log in with the default admin credentials.
   - Click on `Add Realm` and enter a name for your realm (e.g., `Gaurav`).

3. **Create a Client**

   - Select the newly created realm.
   - Go to `Clients` and click `Create`.
   - Enter `test-web-app` as the Client ID and select `openid-connect` as the Client Protocol.
   - Set the `Access Type` to `confidential` and click `Save`.

4. **Configure the Client**

   - In the `Settings` tab, set the `Valid Redirect URIs` to `http://localhost:5000/*` and `Web Origins` to `http://localhost:5000`.
   - Go to the `Credentials` tab to obtain the `Client Secret`. 

5. **Update `config.py`**

   Ensure the Keycloak configuration in `config.py` matches the values you set up:

   ```python
   keycloak_openid = KeycloakOpenID(
       server_url='http://localhost:8080/auth',
       client_id='test-web-app',
       realm_name='Gaurav',
       client_secret_key='your_client_secret'
   )
   ```

## API Endpoints Setup

1. **Start the Application**

   Run the Flask application with:

   ```bash
   python app.py
   ```

   The application will be accessible at `http://localhost:5000`.

2. **GraphQL Endpoint**

   Access the GraphQL interface at `http://localhost:5000/graphql` to interact with the API using GraphiQL.

3. **Stripe Integration**

   The Stripe payment button is included in the `index.html`. Ensure that you use the correct `data-key` for the Stripe public key.

## Usage

- **Home Page**: View and manage your todo items.
- **GraphQL Endpoint**: Use GraphiQL to interact with the API.
- **Stripe Payment**: Use the Stripe button on the homepage to simulate a payment.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to contribute.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.