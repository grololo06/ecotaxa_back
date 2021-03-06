# -*- coding: utf-8 -*-
# This file is part of Ecotaxa, see license.md in the application root directory for license informations.
# Copyright (C) 2015-2020  Picheral, Colin, Irisson (UPMC-CNRS)
#
from sqlalchemy import Index, Column, ForeignKey, Sequence
from sqlalchemy.dialects.postgresql import BIGINT, VARCHAR, INTEGER
from sqlalchemy.engine import ResultProxy
from sqlalchemy.orm import Session

from db.Model import Model


# TODO: Why the ORM does not generate a DEFAULT?
class Image(Model):
    __tablename__ = 'images'
    imgid = Column(BIGINT, Sequence('seq_images'), primary_key=True)
    # The Object that this image belongs to
    # TODO: It looks like we have a relationship cycle Object->Image->Object
    #  Probably due to the fact that several images can exist for a single Object
    # Real PK: objid + imgrank or better orig_id + imgrank
    objid = Column(BIGINT, ForeignKey('obj_head.objid'))
    imgrank = Column(INTEGER)
    file_name = Column(VARCHAR(255))
    orig_file_name = Column(VARCHAR(255))
    width = Column(INTEGER)
    height = Column(INTEGER)
    thumb_file_name = Column(VARCHAR(255))
    thumb_width = Column(INTEGER)
    thumb_height = Column(INTEGER)

    @staticmethod
    def fetch_existing_images(session: Session, prj_id):
        """
            Get all object/image pairs from the project
        """
        ret = set()
        res: ResultProxy = session.execute(
            # Must be reloaded from DB, as phase 1 added all objects for duplicates checking
            "SELECT concat(o.orig_id,'*',i.orig_file_name) "
            "  FROM images i "
            "  JOIN objects o ON i.objid = o.objid "
            " WHERE o.projid= :prj",
            {"prj": prj_id})
        for rec in res:
            ret.add(rec[0])
        return ret


Index('IS_ImagesObjects', Image.objid)
