import click

from biocatalyzer.bioreactor import BioReactor
from biocatalyzer.ms_matcher.ms_data_matcher import MSDataMatcher


@click.command()
@click.argument("compounds",
                type=str,
                required=True,
                )
@click.argument("output_path",
                type=click.Path(),
                required=True,
                )
@click.option("--neutralize",
              "neutralize",
              type=bool,
              default=False,
              help="Whether to neutralize input compounds and newly generated compounds.")
@click.option("--reaction_rules",
              "reaction_rules",
              type=click.Path(exists=True),
              default=None,
              help="The path to the user defined file containing the reaction rules to use.",
              )
@click.option("--organisms",
              "organisms",
              type=click.Path(exists=True),
              default=None,
              help="The path to the user defined file containing the organisms to filter the reaction rules.",
              )
@click.option("--patterns_to_remove",
              "patterns_to_remove",
              type=click.Path(exists=True),
              default=None,
              show_default=True,
              help="A user defined file containing SMARTS patterns. Products that match a pattern will be removed.",
              )
@click.option("--molecules_to_remove",
              "molecules_to_remove",
              type=click.Path(exists=True),
              default=None,
              show_default=True,
              help="A user defined file containing molecules encoded as SMILES to be removed from the products.",
              )
@click.option("--min_atom_count",
              "min_atom_count",
              type=int,
              default=5,
              show_default=True,
              help="The minimum atom count of a molecule (molecules with less atoms are removed from the products).",
              )
@click.option("--ms_data_path",
              "ms_data_path",
              type=click.Path(exists=True),
              default=None,
              show_default=True,
              help="The path to the file containing the MS data to use.")
@click.option("--mode",
              "mode",
              type=click.Choice(['mass', 'mass_diff']),
              default='mass',
              show_default=True,
              help="The mode to use for the MS data matching (mass for ExactMass matching or mass_dif for ExactMass "
                   "differences matching).")
@click.option("--ms_field",
              "ms_field",
              type=str,
              default='Mass',
              show_default=True,
              help="The name of the column to use for the MS data matching.")
@click.option("--tolerance",
              "tolerance",
              type=float,
              default=0.02,
              show_default=True,
              help="The mass tolerance to use when matching MS data.",
              )
@click.option("--n_jobs",
              "n_jobs",
              type=int,
              default=1,
              show_default=True,
              help="The number of jobs to run in parallel.",
              )
def main(compounds,
         output_path,
         reaction_rules,
         neutralize,
         organisms,
         patterns_to_remove,
         molecules_to_remove,
         min_atom_count,
         ms_data_path,
         mode,
         ms_field,
         tolerance,
         n_jobs):
    """Run the biocatalyzer.

    Mandatory arguments:

        compounds: Path to the file containing the compounds to use.

        output_path: Path to the output directory.
    """
    br = BioReactor(compounds_path=compounds,
                    output_path=output_path,
                    neutralize_compounds=neutralize,
                    organisms_path=organisms,
                    patterns_to_remove_path=patterns_to_remove,
                    molecules_to_remove_path=molecules_to_remove,
                    min_atom_count=min_atom_count,
                    n_jobs=n_jobs)
    br.react()

    ms = MSDataMatcher(ms_data_path=ms_data_path,
                       output_path=output_path,
                       mode=mode,
                       ms_field=ms_field,
                       tolerance=tolerance,
                       reaction_rules=br.reaction_rules,
                       new_compounds=br.new_compounds)

    ms.generate_ms_results()


if __name__ == "__main__":
    main()
