import streamlit as st
import pandas as pd
from core.trainer import (
    Trainer,
    TrainingConfig
)


# Session state
if "active_project" not in st.session_state:
    st.session_state.active_project = None

if "training_result" not in st.session_state:
    st.session_state.training_result = None


st.title("🧠 Model Training")


# Check project selection
if not st.session_state.active_project:

    st.warning(
        "Please open a project from Project Workspace first."
    )

    st.stop()


project = st.session_state.active_project


st.success(
    f"Training Project: {project['name']} "
    f"(ID: {project['id']})"
)


st.divider()


st.header("⚙ Training Configuration")

col1, col2 = st.columns(2)


with col1:

    architecture = st.selectbox(
        "Model Architecture",
        [
            "resnet18",
            "mobilenet_v3_small",
            "efficientnet_b0"
        ]
    )


    epochs = st.number_input(
        "Epochs",
        min_value=1,
        max_value=500,
        value=10
    )


    batch_size = st.selectbox(
        "Batch Size",
        [8, 16, 32, 64],
        index=2
    )


with col2:

    learning_rate = st.number_input(
        "Learning Rate",
        min_value=0.00001,
        max_value=1.0,
        value=0.001,
        format="%.5f"
    )


    image_size = st.selectbox(
        "Image Size",
        [128, 224, 256, 512],
        index=1
    )


    augmentation = st.checkbox(
        "Enable Augmentation",
        value=True
    )


with st.expander(
    "🔬 Advanced Settings"
):

    optimizer = st.selectbox(
        "Optimizer",
        [
            "adam",
            "sgd"
        ]
    )


    weight_decay = st.number_input(
        "Weight Decay",
        min_value=0.0,
        value=0.0001,
        format="%.5f"
    )


    freeze_backbone = st.checkbox(
        "Freeze Backbone",
        value=True
    )

st.divider()


if st.button(
    "🚀 Start Training",
    type="primary"
):

    with st.spinner(
        "Training model... This may take a while."
    ):

        try:

            config = TrainingConfig(
                epochs=epochs,
                batch_size=batch_size,
                learning_rate=learning_rate,
                image_size=image_size,
                augmentation=augmentation,

                architecture=architecture,

                optimizer=optimizer,
                weight_decay=weight_decay,
                freeze_backbone=freeze_backbone
            )


            trainer = Trainer(
                config
            )


            result = trainer.train(
                project["id"]
            )


            st.session_state.training_result = result


            st.success(
                "Training completed successfully!"
            )


        except Exception as e:

            st.error(
                f"Training failed: {e}"
            )


# ============================
# Training Results
# ============================

if st.session_state.training_result:

    result = (
        st.session_state.training_result
    )

    history = result["history"]

    model = result["model"]

    st.divider()

    st.header(
        "📊 Training Results"
    )

    st.subheader(
        "Model Information"
    )

    st.info(
        f"""
    Model ID: {model["id"]}

    Model Name: {model["name"]}

    Created: {model["created_at"]}
    """
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Training Accuracy",
            f"{model['metrics']['train_accuracy']:.2f}%"
        )

        st.metric(
            "Training Loss",
            f"{model['metrics']['train_loss']:.4f}"
        )


    with col2:

        st.metric(
            "Validation Accuracy",
            f"{model['metrics']['validation_accuracy']:.2f}%"
        )

        st.metric(
            "Validation Loss",
            f"{model['metrics']['validation_loss']:.4f}"
        )

    st.subheader(
        "Accuracy Over Epochs"
    )


    accuracy_df = pd.DataFrame({
        "Training": history["train_accuracy"],
        "Validation": history["val_accuracy"]
    })


    st.line_chart(
        accuracy_df
    )


    st.subheader(
        "Loss Over Epochs"
    )


    loss_df = pd.DataFrame({
        "Training": history["train_loss"],
        "Validation": history["val_loss"]
    })


    st.line_chart(
        loss_df
    )