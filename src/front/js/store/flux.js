const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			message: null,
			demo: [
				{
					title: "FIRST",
					background: "white",
					initial: "white"
				},
				{
					title: "SECOND",
					background: "white",
					initial: "white"
				}
			]
		},
		actions: {
			// Use getActions to call a function within a fuction
			exampleFunction: () => {
				getActions().changeColor(0, "green");
			},

			getMessage: async () => {
				try {
					// fetching data from the backend
					const resp = await fetch(process.env.BACKEND_URL + "api/hello")
					const data = await resp.json()
					setStore({ message: data.message })
					// don't forget to return something, that is how the async resolves
					return data;
				} catch (error) {
					console.log("Error loading message from backend", error)
				}
			},
			changeColor: (index, color) => {
				//get the store
				const store = getStore();

				//we have to loop the entire demo array to look for the respective index
				//and change its color
				const demo = store.demo.map((elm, i) => {
					if (i === index) elm.background = color;
					return elm;
				});

				//reset the global store
				setStore({ demo: demo });
			},
			signUp: async (email, password, passwordConfirmation) => {
				const bodyData = {
					email: email,
					password: password,
					passwordConfirmation: passwordConfirmation
				}
				
				const options = {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					}, 
					body: JSON.stringify(bodyData)
				};

				try {
					console.log("Getting backend url")
					console.log(process.env.BACKEND_URL)
					// fetching data from the backend
					const response = await fetch(`${process.env.BACKEND_URL}/api/sign_up`, options);
					
					
					const msg = await response.json();
					console.log(msg)

					// don't forget to return something, that is how the async resolves
					return msg;
				} catch (error) {
					console.log("Error loading message from backend", error)
				}
			},
			signIn: async (email, password) => {
				try {

					const bodyData = {
						email: email,
						password: password,
					}

					const options = {
						method: 'POST',
						headers: {
							'Content-Type': 'application/json'
						},
						body: JSON.stringify(bodyData)
					};
					
					// fetching data from the backend
					const response = await fetch(`${process.env.BACKEND_URL}/api/sign_in`, options);
					const msg = await response.json()

					// don't forget to return something, that is how the async resolves
					return msg;
				} catch (error) {
					console.log("Error loading message from backend", error)
				}
			}
		}
	};
};

export default getState;
