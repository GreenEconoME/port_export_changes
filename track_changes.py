# Import dependencies
import yaml
import traceback
import streamlit as st
import pandas as pd

from datetime import datetime

# Import helper functions
from utilities.download_image_from_github import download_image_from_github
from utilities.generate_report import gen_report
from utilities.static_vars import unique_keys, sheets_to_compare
from utilities.formatting import display_progress_list


# Import the secrets
access_token = st.secrets["GITHUB_TOKEN"]
repo_owner = st.secrets['REPO_OWNER']
repo_name = st.secrets['REPO_NAME']
branch = st.secrets['BRANCH']
image_path = st.secrets['IMAGE_PATH']
credential_key = st.secrets['CREDENTIAL_KEY']


# Download and display the logo
logo_image = download_image_from_github(repo_owner, repo_name, image_path, branch, access_token)
if logo_image:
    st.image(logo_image, use_column_width=True)

# Set a title for the page
st.markdown("<h2 style = 'text-align: center; color: black;'>Dashboard Portfolio Export</br>What's Changed?</h2>", unsafe_allow_html = True)


# Handle credential file upload
st.subheader("Upload Credentials")
cred_upload = st.file_uploader("Upload credentials file (crecential_key.yaml)", type = "yaml")
if cred_upload is not None:
    try:
        credentials = yaml.safe_load(cred_upload)

        # Get credential key from credential file
        yaml_credential = credentials.get('credential_key')
        if yaml_credential == credential_key:

            st.subheader("Upload Old Report")
            old_upload = st.file_uploader("Upload the older portfolio export.", type="xlsx")

            st.subheader("Upload New Report")
            new_upload = st.file_uploader("Upload the new portfolio export.", type="xlsx")



            # Ensure both reports have been uploaded
            if old_upload is not None and new_upload is not None:
                if st.button('Click to start processing differences'):
                    # Initialize progress tracking with file loading
                    st.session_state["sheet_status"] = {
                        "Loading Old Report": "Pending",
                        "Loading New Report": "Pending",
                        **{sheet: "Pending" for sheet in sheets_to_compare},
                        "Generating Download": "Pending"
                    }

                    # Create a placeholder for progress updates
                    progress_placeholder = st.empty()
                    progress_placeholder.markdown(display_progress_list(st.session_state["sheet_status"]))

                    # Read in the workbooks
                    # Start loading OLD report
                    st.session_state["sheet_status"]["Loading Old Report"] = "Processing"
                    progress_placeholder.markdown(display_progress_list(st.session_state["sheet_status"]))
                    with pd.ExcelFile(old_upload) as f:
                        old = pd.read_excel(f, sheet_name = None)

                    # Set reading in old report as completed
                    st.session_state["sheet_status"]["Loading Old Report"] = "Completed"
                    progress_placeholder.markdown(display_progress_list(st.session_state["sheet_status"]))

                    # Start loading NEW report
                    st.session_state["sheet_status"]["Loading New Report"] = "Processing"
                    progress_placeholder.markdown(display_progress_list(st.session_state["sheet_status"]))

                    with pd.ExcelFile(new_upload) as f:
                        new = pd.read_excel(f, sheet_name = None)

                    # Set reading in the new report as completed
                    st.session_state["sheet_status"]["Loading New Report"] = "Completed"
                    progress_placeholder.markdown(display_progress_list(st.session_state["sheet_status"]))

                    # Remove column not needing comparison
                    old['Meter Activity'].drop(columns = [x for x in old['Meter Activity'].columns if 'Days Since Upload as of' in x], inplace = True)
                    new['Meter Activity'].drop(columns = [x for x in new['Meter Activity'].columns if 'Days Since Upload as of' in x], inplace = True)

                    # Generate the what's changed report
                    result = gen_report(unique_keys, sheets_to_compare, progress_placeholder, old, new)

                    # Store result in session_state to prevent rerunning upon download
                    st.session_state['changed_report'] = result

                    # Offer the file for download
                    if 'changed_report' in st.session_state:
                        st.download_button(
                            label = "Download What's Changed Report",
                            data = st.session_state["changed_report"],
                            file_name = f"{datetime.now().strftime('%Y-%m-%d')} Changes.xlsx",
                            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                        )

                        # set generating export to completed
                        st.session_state["sheet_status"]["Generating Download"] = "Completed"
                        progress_placeholder.markdown(display_progress_list(st.session_state["sheet_status"]))

        else:
            st.error('Invalid credentials.')
    except Exception as e:
        st.write(traceback.print_exc())
else:
    st.write('Please upload the credentials file.')
