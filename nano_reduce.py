# ============================================================
#              Developed by Bapi Basak
#                    IISER Pune
#                   August 2026
# ============================================================


import argparse

from core.reducer import NanoReducer
from core.writer import NanoWriter
import importlib.util

parser = argparse.ArgumentParser(
    description="Run NanoReducer on a NanoAOD ROOT file.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    epilog="""
Examples:
  python run.py --input input.root --output skim.root --config core/config.py

  python run.py --input input.root --config core/config_data.py --data
"""
)

parser.add_argument("--input", required=True)
parser.add_argument("--output", default="skim.root")

parser.add_argument(
    "--config",
    required=True,
    help="Path to the Python config file.",
)

parser.add_argument(
    "--apply-jet-selection",
    action="store_true",
    help="Apply jet selection.",
)

parser.add_argument(
    "--apply-electron-selection",
    action="store_true",
    help="Apply electron selection.",
)

parser.add_argument(
    "--apply-muon-selection",
    action="store_true",
    help="Apply muon selection.",
)

parser.add_argument(
    "--apply-photon-selection",
    action="store_true",
    help="Apply photon selection.",
)

parser.add_argument(
    "--apply-event-selection",
    action="store_true",
    help="Apply event selection.",
)

parser.add_argument(
    "--data",
    action="store_true",
    help="Process data instead of MC.",
)

parser.add_argument(
    "--apply_trigger",
    action="store_true",
    help="Apply the configured HLT trigger selection.",
)

parser.add_argument(
    "--apply_pixelSeed",
    action="store_true",
    help="Apply the pixelSeed selection on photons.",
)

parser.add_argument(
    "--apply_bJet_tagger",
    action="store_true",
    help="Apply the bJet_tagger selection.",
)

parser.add_argument(
    "--apply_kinematic_cuts_jet",
    action="store_true",
    help="Apply the bJet_tagger selection.",
)

args = parser.parse_args()

def load_config(config_path):
    spec = importlib.util.spec_from_file_location("user_config", config_path)

    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load config: {config_path}")

    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    return config

config = load_config(args.config)
data_kind = "data" if args.data else "mc"

store = NanoReducer(
    args.input,
    config=config,
    jet_selection=args.apply_jet_selection,
    electron_selection=args.apply_electron_selection,
    muon_selection=args.apply_muon_selection,
    photon_selection=args.apply_photon_selection,
    event_selection=args.apply_event_selection,
    apply_trigger=args.apply_trigger, 
    apply_pixelSeed=args.apply_pixelSeed,
    apply_bJet_tagger=args.apply_bJet_tagger,
    apply_kinematic_cuts_jet=args.apply_kinematic_cuts_jet
).run()

NanoWriter(args.output, config=config, data_kind=data_kind).write(store)