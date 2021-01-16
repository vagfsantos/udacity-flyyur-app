"""empty message

Revision ID: a0d6796570d3
Revises: 3040eff26a22
Create Date: 2021-01-16 15:32:34.137436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0d6796570d3'
down_revision = '3040eff26a22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    genres_table = op.create_table('Genre',
                                   sa.Column('id', sa.Integer(),
                                             nullable=False),
                                   sa.Column('name', sa.String(),
                                             nullable=False),
                                   sa.PrimaryKeyConstraint('id')
                                   )
    op.create_table('ArtistGenres',
                    sa.Column('genre_id', sa.Integer(), nullable=False),
                    sa.Column('artist_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
                    sa.ForeignKeyConstraint(['genre_id'], ['Genre.id'], ),
                    sa.PrimaryKeyConstraint('genre_id', 'artist_id')
                    )
    op.create_table('VenueGenres',
                    sa.Column('genre_id', sa.Integer(), nullable=False),
                    sa.Column('venue_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['genre_id'], ['Genre.id'], ),
                    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
                    sa.PrimaryKeyConstraint('genre_id', 'venue_id')
                    )
    op.bulk_insert(genres_table,  [
        {'name': 'Alternative'},
        {'name': 'Blues'},
        {'name': 'Classical'},
        {'name': 'Country'},
        {'name': 'Electronic'},
        {'name': 'Folk'},
        {'name': 'Funk'},
        {'name': 'Hip-Hop'},
        {'name': 'Heavy Metal'},
        {'name': 'Instrumental'},
        {'name': 'Jazz'},
        {'name': 'Musical Theatre'},
        {'name': 'Pop'},
        {'name': 'Punk'},
        {'name': 'R&B'},
        {'name': 'Reggae'},
        {'name': 'Rock n Roll'},
        {'name': 'Soul'},
        {'name': 'Other'}
    ])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('VenueGenres')
    op.drop_table('ArtistGenres')
    op.drop_table('Genre')
    # ### end Alembic commands ###
